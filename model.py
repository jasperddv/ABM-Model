# Importing necessary libraries
import networkx as nx
from mesa import Model, Agent
from mesa.time import SimultaneousActivation
from mesa.space import NetworkGrid
from mesa.datacollection import DataCollector
import geopandas as gpd
import rasterio as rs
import matplotlib.pyplot as plt
import random

# Import the agent class(es) from agents.py
from agents import Households, Government, Waterboard, Insurance_company, Policy_maker

# Import functions from functions.py
from functions import get_flood_map_data, calculate_basic_flood_damage
from functions import map_domain_gdf, floodplain_gdf

#from run_tests import ScenarioNO

# Define the AdaptationModel class
class AdaptationModel(Model):
    """
    The main model running the simulation. It sets up the network of household agents,
    simulates their behavior, and collects data. The network type can be adjusted based on study requirements.
    """

    def __init__(self, 
                 seed = None,
                 number_of_households = 25, # number of household agents
                 # Simplified argument for choosing flood map. Can currently be "harvey", "100yr", or "500yr".
                 flood_map_choice='harvey',
                 # ### network related parameters ###
                 # The social network structure that is used.
                 # Can currently be "erdos_renyi", "barabasi_albert", "watts_strogatz", or "no_network"
                 network = 'watts_strogatz',
                 # likeliness of edge being created between two nodes
                 probability_of_network_connection = 0.4,
                 # number of edges for BA network
                 number_of_edges = 3,
                 # number of nearest neighbours for WS social network
                 number_of_nearest_neighbours = 5,
                 political_situation = 5,
                 welfare = 5,
                 scenarioNO = 0,
                 ):
        
        super().__init__(seed = seed)

        #unique id counter to ensure unique id for each agent
        self.unique_id_counter = 0

        # defining the variables and setting the values
        self.number_of_households = number_of_households  # Total number of household agents
        self.seed = seed

        # network
        self.network = network # Type of network to be created
        self.probability_of_network_connection = probability_of_network_connection
        self.number_of_edges = number_of_edges
        self.number_of_nearest_neighbours = number_of_nearest_neighbours

        # generating the graph according to the network used and the network parameters specified
        self.G = self.initialize_network()
        # create grid out of network graph
        self.grid = NetworkGrid(self.G)

        # Initialize maps
        self.initialize_maps(flood_map_choice)

        # set schedule for agents
        self.schedule = SimultaneousActivation(self)  # Schedule for activating agents

        # check if political_situation has correct value (between 0 and 1) as input
        if political_situation > 1 or political_situation < 0:
            # if not, generate random value between 0 and 1 for political situation
            self.political_situation = random.random()
        else:
            #copy input value to model value
            self.political_situation = political_situation

        # check if welfare has correct value (between 0 and 1) as input
        if welfare > 1 or welfare < 0:
            # if not, generate random value between 0 and 1 for welfare
            self.welfare = random.randint(0,1)
        else:
            # copy input value to model value
            self.welfare = welfare

        # give scenario number as value to model
        self.scenarioNO = scenarioNO

        # create households through initiating a household on each node of the network graph
        for i, node in enumerate(self.G.nodes()):
            household = Households(unique_id=self.unique_id_counter, model=self, political_situation=self.political_situation, welfare = self.welfare)
            # unique id counter +1 to ensure unique id for next agent created
            self.unique_id_counter = self.unique_id_counter + 1
            self.schedule.add(household)
            self.grid.place_agent(agent=household, node_id=node)

        # initialise government agent
        self.government = Government(unique_id=self.unique_id_counter, model=self, welfare=self.welfare, political_situation=self.political_situation)
        self.schedule.add(self.government)
        # unique id counter +1 to ensure unique id for next agent created
        self.unique_id_counter = self.unique_id_counter + 1

        # initialise waterboard agent
        self.waterboard = Waterboard(unique_id=self.unique_id_counter, model=self, welfare=self.welfare,
                                political_situation=self.political_situation)
        self.schedule.add(self.waterboard)
        # unique id counter +1 to ensure unique id for next agent created
        self.unique_id_counter = self.unique_id_counter + 1

        # initialise insurance_company agent
        self.insurance_company = Insurance_company(unique_id=self.unique_id_counter, model=self)
        self.schedule.add(self.insurance_company)
        # unique id counter +1 to ensure unique id for next agent created
        self.unique_id_counter = self.unique_id_counter + 1

        # initialise policy_maker agent
        self.policy_maker = Policy_maker(unique_id=self.unique_id_counter, model=self)
        self.schedule.add(self.policy_maker)

        # Data collection setup to collect data
        model_metrics = {
                        "total_adapted_households": self.total_adapted_households,
                        "provide_information": self.provide_information,
                        "subsidies": self.subsidies,
                        "regulation": self.regulation,
                        "infrastructure_government": self.infrastructure_government,
                        "PoliticalSituation": self.determine_political_situation
                        # ... other reporters ...
                        }
        
        agent_metrics = {
                        "FloodDepthEstimated": "flood_depth_estimated",
                        "FloodDamageEstimated" : "flood_damage_estimated",
                        "FloodDepthActual": "flood_depth_actual",
                        "FloodDamageActual" : "flood_damage_actual",
                        "IsAdapted": "is_adapted",
                        "FriendsCount": lambda a: a.count_friends(radius=1),
                        "location":"location",
                        "SandbagsPlaced":"sandbags_placed",
                        "InsuranceTaken":"insurance_taken_by_household",
                        "HouseholdAttitude":"household_attitude"
                        # ... other reporters ...
                        }
        #set up the data collector 
        self.datacollector = DataCollector(model_reporters=model_metrics, agent_reporters=agent_metrics)

    def initialize_network(self):
        """
        Initialize and return the social network graph based on the provided network type using pattern matching.
        """
        if self.network == 'erdos_renyi':
            return nx.erdos_renyi_graph(n=self.number_of_households,
                                        p=self.number_of_nearest_neighbours / self.number_of_households,
                                        seed=self.seed)
        elif self.network == 'barabasi_albert':
            return nx.barabasi_albert_graph(n=self.number_of_households,
                                            m=self.number_of_edges,
                                            seed=self.seed)
        elif self.network == 'watts_strogatz':
            return nx.watts_strogatz_graph(n=self.number_of_households,
                                        k=self.number_of_nearest_neighbours,
                                        p=self.probability_of_network_connection,
                                        seed=self.seed)
        elif self.network == 'no_network':
            G = nx.Graph()
            G.add_nodes_from(range(self.number_of_households))
            return G
        else:
            raise ValueError(f"Unknown network type: '{self.network}'. "
                            f"Currently implemented network types are: "
                            f"'erdos_renyi', 'barabasi_albert', 'watts_strogatz', and 'no_network'")


    def initialize_maps(self, flood_map_choice):
        """
        Initialize and set up the flood map related data based on the provided flood map choice.
        """
        # Define paths to flood maps
        flood_map_paths = {
            'harvey': r'../input_data/floodmaps/Harvey_depth_meters.tif',
            '100yr': r'../input_data/floodmaps/100yr_storm_depth_meters.tif',
            '500yr': r'../input_data/floodmaps/500yr_storm_depth_meters.tif'  # Example path for 500yr flood map
        }

        # Throw a ValueError if the flood map choice is not in the dictionary
        if flood_map_choice not in flood_map_paths.keys():
            raise ValueError(f"Unknown flood map choice: '{flood_map_choice}'. "
                             f"Currently implemented choices are: {list(flood_map_paths.keys())}")

        # Choose the appropriate flood map based on the input choice
        flood_map_path = flood_map_paths[flood_map_choice]

        # Loading and setting up the flood map
        self.flood_map = rs.open(flood_map_path)
        self.band_flood_img, self.bound_left, self.bound_right, self.bound_top, self.bound_bottom = get_flood_map_data(
            self.flood_map)

    def total_adapted_households(self):
        """Return the total number of households that have adapted."""
        #BE CAREFUL THAT YOU MAY HAVE DIFFERENT AGENT TYPES SO YOU NEED TO FIRST CHECK IF THE AGENT IS ACTUALLY A HOUSEHOLD AGENT USING "ISINSTANCE"
        adapted_count = sum([1 for agent in self.schedule.agents if isinstance(agent, Households) and agent.is_adapted])
        return adapted_count

    #here, the policy maker is called to determine the new value of provide_information
    def provide_information(self):
        return self.policy_maker.provide_information

    #here, the policy maker is called to determine the new value of subsidies
    def subsidies(self):
        return self.policy_maker.subsidies

    #here, the policy maker is called to determine the new value of regulation
    def regulation(self):
        return self.policy_maker.regulation

    #here, the policy maker is called to determine the new value of infrastructure government
    def infrastructure_government(self):
        return self.policy_maker.infrastructure_government

    #here, the new political situation is determined
    def determine_political_situation(self):
        return self.political_situation
    
    def plot_model_domain_with_agents(self):
        fig, ax = plt.subplots()
        # Plot the model domain
        map_domain_gdf.plot(ax=ax, color='lightgrey')
        # Plot the floodplain
        floodplain_gdf.plot(ax=ax, color='lightblue', edgecolor='k', alpha=0.5)

        # Collect agent locations and statuses
        for agent in self.schedule.agents:
            #only execute code for households
            if type(agent) == Households:
                color = 'blue' if agent.is_adapted else 'red'
                ax.scatter(agent.location.x, agent.location.y, color=color, s=10, label=color.capitalize() if not ax.collections else "")
                ax.annotate(str(agent.unique_id), (agent.location.x, agent.location.y), textcoords="offset points", xytext=(0,1), ha='center', fontsize=9)
        # Create legend with unique entries
        handles, labels = ax.get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        ax.legend(by_label.values(), by_label.keys(), title="Red: not adapted, Blue: adapted")

        # Customize plot with titles and labels
        plt.title(f'Model Domain with Agents at Step {self.schedule.steps}')
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.show()

    def determine_average_political_perception_households(self):
        #function used to determine the average political perception of the households
        #this function is called in the step of government to be used to determine the government their new political perception

        #reset value
        self.average_political_perception_households = 0

        # loop through all agents
        for agent in self.schedule.agents:
            #only execute code for households
            if type(agent) == Households:
                #sum all political perceptions
                self.average_political_perception_households = self.average_political_perception_households + agent.political_perception
        #return the average political perception by dividing by the total number of households
        return self.average_political_perception_households/self.number_of_households

    def step(self):
        """
        introducing a shock: 
        at time step 5, there will be a global flooding.
        This will result in actual flood depth. Here, we assume it is a random number
        between 0.5 and 1.2 of the estimated flood depth. In your model, you can replace this
        with a more sound procedure (e.g., you can devide the floop map into zones and 
        assume local flooding instead of global flooding). The actual flood depth can be 
        estimated differently
        """


        for agent in self.schedule.agents:
            # only execute code for households
            if type(agent) == Households:
                agent.flood_depth_actual = agent.flood_depth_actual - random.uniform(0.2,
                                                                                     0.5) * agent.flood_depth_estimated
                if agent.flood_depth_actual < 0:
                    agent.flood_depth_actual = 0
                agent.flood_damage_actual = calculate_basic_flood_damage(agent.flood_depth_actual,
                                                                         agent.sandbags_placed,
                                                                         self.waterboard.adaptation_on_rivers_and_drainages,
                                                                         self.government.warning_system,
                                                                         self.policy_maker.infrastructure_government)
                if self.schedule.steps > 0 and (self.schedule.steps % 5) == 0:
                    # Calculate the actual flood depth as a random number between 0.5 and 1.2 times the estimated flood depth
                    agent.flood_depth_actual = agent.flood_depth_actual + random.uniform(0.4, 0.9) * agent.flood_depth_estimated
                    # calculate the actual flood damage given the actual flood depth
                    agent.flood_damage_actual = calculate_basic_flood_damage(agent.flood_depth_actual, agent.sandbags_placed, self.waterboard.adaptation_on_rivers_and_drainages,
                                                                             self.government.warning_system, self.policy_maker.infrastructure_government)

        # randomly determine if a protest takes place this step, value 0 or 1
        self.protest = random.randint(0,1)

        # Collect data and advance the model by one step
        self.datacollector.collect(self)
        self.schedule.step()


