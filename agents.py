# Importing necessary libraries
import random
from mesa import Agent
from shapely.geometry import Point
from shapely import contains_xy
#from model import AdaptationModel

# Import functions from functions.py
from functions import generate_random_location_within_map_domain, get_flood_depth, calculate_basic_flood_damage, floodplain_multipolygon


# Define the Households agent class
class Households(Agent):
    """
    An agent representing a household in the model.
    Each household has a flood depth attribute which is randomly assigned for demonstration purposes.
    In a real scenario, this would be based on actual geographical data or more complex logic.
    """

    def __init__(self, unique_id, model, political_situation, welfare):
        super().__init__(unique_id, model)

        #import all functions of the model to be able to use them in Government
        self.main_model = model

        # Initial adaptation status set to False, determines whether an agent is going to adapt and the colour of the agent on the map
        self.is_adapted = False

        # set welfare value
        self.welfare = welfare

        #initalise attitude to 0
        self.household_attitude = 0

        # initialise sandbags placed by household
        self.sandbags_placed = 0

        # initialise for all households in a way that they do not have an insurance first
        self.insurance_taken_by_household = 0

        # determine value of house to convert flood damages to monetary damages
        self.value_house = random.randrange(200, 1500, 1) * 1000

        # getting flood map values
        # Get a random location on the map
        loc_x, loc_y = generate_random_location_within_map_domain()
        self.location = Point(loc_x, loc_y)

        # Check whether the location is within floodplain
        # Where is this used?
        self.in_floodplain = False
        if contains_xy(geom=floodplain_multipolygon, x=self.location.x, y=self.location.y):
            self.in_floodplain = True

        # Get the estimated flood depth at those coordinates. 
        # the estimated flood depth is calculated based on the flood map (i.e., past data) so this is not the actual flood depth
        # Flood depth can be negative if the location is at a high elevation
        self.flood_depth_estimated = get_flood_depth(corresponding_map=model.flood_map, location=self.location, band=model.band_flood_img)
        # handle negative values of flood depth
        if self.flood_depth_estimated < 0:
            self.flood_depth_estimated = 0
        
        # calculate the estimated flood damage given the estimated flood depth. Flood damage is a factor between 0 and 1
        #add some uncertaintity to estimation with the random factor at the end
        self.flood_damage_estimated = calculate_basic_flood_damage(flood_depth=self.flood_depth_estimated, sandbags_household=self.sandbags_placed,
                                                                   waterboard_adaptation=0,
                                                                   warning_system_government=0,
                                                                   infrastructure=0) + random.randrange(-10, 10, 1)/100

        #compute estimated monetary flood damages
        #damages are lowered by 70% if insurance is taken
        if self.insurance_taken_by_household == 1:
            self.monetary_damage_estimated = self.flood_damage_estimated * self.value_house * 0.3
        else:
            self.monetary_damage_estimated = self.flood_damage_estimated * self.value_house

        # Add an attribute for the actual flood depth. This is set to zero at the beginning of the simulation since there is not flood yet
        # and will update its value when there is a shock (i.e., actual flood). Shock happens at some point during the simulation
        self.flood_depth_actual = 0
        
        #calculate the actual flood damage given the actual flood depth. Flood damage is a factor between 0 and 1
        self.flood_damage_actual = calculate_basic_flood_damage(flood_depth=self.flood_depth_actual, sandbags_household=self.sandbags_placed,
                                                                   waterboard_adaptation=0,
                                                                   warning_system_government=0,
                                                                   infrastructure=0)

        #compute actual monetary flood damages
        #damages are lowered by 70% if insurance is taken
        if self.insurance_taken_by_household == 1:
            self.monetary_damage_actual = self.flood_damage_actual * self.value_house * 0.3
        else:
            self.monetary_damage_actual = self.flood_damage_actual * self.value_house

        # political perception of household is determined by political situation + a random value between -0.3 and 0.3.
        # If political perception value is above 1, it will be put to 1. If it is below 0, it is put to 0
        self.political_perception = political_situation + random.randrange(-30, 30, 1)/100
        if self.political_perception > 1:
            self.political_perception = 1
        elif self.political_perception < 0:
            self.political_perception = 0

        #create list that contains flood damage over the past years, used to create household attitude
        self.past_flood_damages = [0, 0, 0, 0]
        self.past_flood_damages.append(self.flood_damage_actual)

    # Function to count friends who can be influencial.
    def count_friends(self, radius):
        """Count the number of neighbors within a given radius (number of edges away). This is social relation and not spatial"""
        self.friends = self.model.grid.get_neighbors(self.pos, include_center=False)
        return len(self.friends)

    def step(self):
        # Logic for adaptation based on estimated flood damage and a random chance.
        # These conditions are examples and should be refined for real-world applications.
        if self.flood_damage_estimated > 0.15 and random.random() < 0.2:
            self.is_adapted = True  # Agent adapts to flooding

        #append past_flood_damages list with the new actual flood damage
        self.past_flood_damages.append(self.flood_damage_actual)

        #compute household attitude using the average value of the last 5 values past_flood_damages list
        self.household_attitude = sum(self.past_flood_damages[-5:])/5

        #determine savings of household
        self.savings_household = 2000 + self.welfare*1000*random.randint(0,10)

        #create list with political perception of neighbours
        self.friends_political_perceptions_neighbours = []
        for friend in range(len(self.friends)):
            self.friends_political_perceptions_neighbours.append(self.friends[friend].political_perception)

        #compute average poliitcal perception of neighbours
        self.average_political_perception_neighbours = sum(self.friends_political_perceptions_neighbours)/len(self.friends)

        #compute new value for political perception based upon own political peeception and the average political perception of neighbours
        self.political_perception = 0.3*self.political_perception + 0.7*self.average_political_perception_neighbours

        #insurance willingness
        #insurance media activity
        for agent in self.main_model.schedule.agents:
            # only execute code for insurance company
            if type(agent) == Insurance_company:
                self.insurance_willingness = agent.determine_willingness_to_provide_insurance(self)
                self.insurance_company_media_platform_usage = agent.media_platform_usage

        #determine if this household takes an insurance of this time period
        self.insurance_taken_by_household = (0.3*self.main_model.subsidies + 0.3*self.insurance_willingness +
                                             0.3*self.insurance_company_media_platform_usage + 0.5*self.main_model.infrastructure_government +
                                             0.1*self.savings_household/1000 + 0.3*self.household_attitude)
        if self.insurance_taken_by_household < 1.5:
            self.insurance_taken_by_household = 0
        else:
            self.insurance_taken_by_household = 1

        #determine sandbags placed by household
        self.sandbags_placed = (2*self.main_model.provide_information + 3*self.main_model.subsidies + 2*self.main_model.regulation -
                                5*self.main_model.infrastructure_government - 3*self.insurance_taken_by_household +
                                1*self.savings_household/1000 + 3*self.household_attitude)

# Define the Government agent class
class Government(Agent):
    def __init__(self, unique_id, model, welfare, political_situation):
        super().__init__(unique_id, model)
        # initialise welfare in the country
        self.welfare = welfare

        # initialise warning system value
        self.warning_system = 0

        #import all functions of the model to be able to use them in Government
        self.main_model = model

        #initialise political perception of the government using the political situation
        self.political_perception_government = political_situation

    #added this to ensure 'agent_metrics' works in model.py. Else FriendsCount does not work in the metrics
    def count_friends(self, radius):
        """Count the number of neighbors within a given radius (number of edges away). This is social relation and not spatial"""
        #Empty list, government has no friends
        friends = []
        return len(friends)

    def determine_political_perception_government(self, political_perception_government, average_political_perception_households):
        # Determine the new political perception of the government
        political_perception_government = (0.5*political_perception_government + 0.5*average_political_perception_households)

        #keep political perception value between bounds, 0 and 1
        if political_perception_government > 1:
            political_perception_government = 1
        elif political_perception_government < 0:
            political_perception_government = 0

        return political_perception_government

    def step(self):
        #Compute average political perception among households,
        self.average_political_perception_households = self.main_model.determine_average_political_perception_households()

        # Determine the new political perception of the government
        self.political_perception_government = self.determine_political_perception_government(self.political_perception_government, self.average_political_perception_households)

        # determine government budget based upon welfare and political perception of the government
        self.government_budget = 0.6*self.welfare + 1.4*self.political_perception_government

        # determine whether government uses a warning system
        self.warning_system = self.main_model.provide_information*3 + self.main_model.regulation*2

# Define the Waterboard agent class
class Waterboard(Agent):
    def __init__(self, unique_id, model, welfare, political_situation):
        super().__init__(unique_id, model)

        #import all functions of the model to be able to use them in Insurance company
        self.main_model = model

        #initialise by giving value 0
        self.adaptation_on_rivers_and_drainages = 0

        # Add an attribute for the actual flood depth. This is set to zero at the beginning of the simulation since there is not flood yet
        # and will update its value when there is a shock (i.e., actual flood). Shock happens at some point during the simulation
        self.flood_depth_actual = 0

        # calculate the actual flood damage given the actual flood depth. Flood damage is a factor between 0 and 1
        self.flood_damage_actual = calculate_basic_flood_damage(flood_depth=self.flood_depth_actual, sandbags_household=0,
                                                                   waterboard_adaptation=self.adaptation_on_rivers_and_drainages,
                                                                   warning_system_government=0.5,
                                                                   infrastructure=0.5)

        #create list that contains flood damage over the past years, used to create household attitude
        self.past_flood_damages = [0, 0, 0, 0]
        self.past_flood_damages.append(self.flood_damage_actual)

        #initialise measures taken by waterboard
        self.adaptation_on_rivers_and_drainages = 0

    #added this to ensure 'agent_metrics' works in model.py. Else FriendsCount does not work in the metrics
    def count_friends(self, radius):
        """Count the number of neighbors within a given radius (number of edges away). This is social relation and not spatial"""
        #Empty list, waterboard has no friends
        friends = []
        return len(friends)

    def step(self):
        #initialise to 0
        self.household_average_flood_damage = 0
        #get average flood damage of households
        for agent in self.main_model.schedule.agents:
            # only execute code for households
            if type(agent) == Households:
                self.household_average_flood_damage = self.household_average_flood_damage + calculate_basic_flood_damage(agent.flood_depth_actual,
                                                                         agent.sandbags_placed,
                                                                         self.adaptation_on_rivers_and_drainages,
                                                                         self.main_model.government.warning_system,
                                                                         self.main_model.infrastructure_government)
        self.household_average_flood_damage = self.household_average_flood_damage / self.main_model.number_of_households
        # append past_flood_damages list with the new actual flood damage
        self.past_flood_damages.append(self.household_average_flood_damage)

        #determine attitude of waterboard based upon past flood damages. The waterboard always has an attitude of at least 0.5
        self.waterboard_attitude = (5 + sum(self.past_flood_damages[-5:])) / 10

        #determine waterboard measure taken
        self.adaptation_on_rivers_and_drainages = self.main_model.provide_information + 3*self.main_model.regulation + 3*self.waterboard_attitude

# Define the Insurance company agent class
class Insurance_company(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

        #import all functions of the model to be able to use them in Insurance company
        self.main_model = model

        #initialise media platform usage
        self.media_platform_usage = random.randint(0, 1)

    #added this to ensure 'agent_metrics' works in model.py. Else FriendsCount does not work in the metrics
    def count_friends(self, radius):
        """Count the number of neighbors within a given radius (number of edges away). This is social relation and not spatial"""
        #Empty list, insurance company has no friends
        friends = []
        return len(friends)

    def determine_willingness_to_provide_insurance(self, household):
        #function to determine if a household is allowed to get an insurance or not
        self.total_policy_value = self.main_model.provide_information + self.main_model.subsidies + self.main_model.regulation + self.main_model.infrastructure_government
        if self.total_policy_value > 2 and household.flood_damage_estimated < 0.6:
            return 1
        else:
            return 0

    def step(self):
        #determine and store willingness to provide insurance per household??

        #determine if insurance_company uses media platform for advertisements
        self.media_platform_usage = random.randint(0,1)
