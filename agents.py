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

    def __init__(self, unique_id, model, political_situation):
        super().__init__(unique_id, model)
        # Initial adaptation status set to False, determines whether an agent is going to adapt and the colour of the agent on the map
        self.is_adapted = False

        #initalise attitude to 0
        self.household_attitude = 0

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
        self.flood_damage_estimated = calculate_basic_flood_damage(flood_depth=self.flood_depth_estimated)

        # Add an attribute for the actual flood depth. This is set to zero at the beginning of the simulation since there is not flood yet
        # and will update its value when there is a shock (i.e., actual flood). Shock happens at some point during the simulation
        self.flood_depth_actual = 0
        
        #calculate the actual flood damage given the actual flood depth. Flood damage is a factor between 0 and 1
        self.flood_damage_actual = calculate_basic_flood_damage(flood_depth=self.flood_depth_actual)

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

        #create list with political perception of neighbours
        self.friends_political_perceptions_neighbours = []
        for friend in range(len(self.friends)):
            self.friends_political_perceptions_neighbours.append(self.friends[friend].political_perception)

        #compute average poliitcal perception of neighbours
        self.average_political_perception_neighbours = sum(self.friends_political_perceptions_neighbours)/len(self.friends)

        #compute new value for political perception based upon own political peeception and the average political perception of neighbours
        self.political_perception = 0.3*self.political_perception + 0.7*self.average_political_perception_neighbours

# Define the Government agent class
class Government(Agent):
    def __init__(self, unique_id, model, welfare, political_situation):
        super().__init__(unique_id, model)
        # initialise welfare in the country
        self.welfare = welfare

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

    def step(self):
        # randomly determine if a protest takes place this step, value 0 or 1
        self.protest = random.randint(0,1)

        # Compute average political perception among households, to determine the new political perception of the government
        self.average_political_perception_households = self.main_model.determine_average_political_perception_households()
        self.political_perception_government = 0.5*self.political_perception_government + 0.5*self.average_political_perception_households

        #keep political perception value between bounds, 0 and 1
        if self.political_perception_government > 1:
            self.political_perception_government = 1
        elif self.political_perception_government < 0:
            self.political_perception_government = 0

        # determine government budget based upon welfare and political perception of the government
        self.government_budget = 0.6*self.welfare + 1.4*self.political_perception_government

# Define the Waterboard agent class
class Waterboard(Agent):
    def __init__(self, unique_id, model, welfare, political_situation):
        super().__init__(unique_id, model)

        # Add an attribute for the actual flood depth. This is set to zero at the beginning of the simulation since there is not flood yet
        # and will update its value when there is a shock (i.e., actual flood). Shock happens at some point during the simulation
        self.flood_depth_actual = 0

        # calculate the actual flood damage given the actual flood depth. Flood damage is a factor between 0 and 1
        self.flood_damage_actual = calculate_basic_flood_damage(flood_depth=self.flood_depth_actual)

        #create list that contains flood damage over the past years, used to create household attitude
        self.past_flood_damages = [0, 0, 0, 0]
        self.past_flood_damages.append(self.flood_damage_actual)

    #added this to ensure 'agent_metrics' works in model.py. Else FriendsCount does not work in the metrics
    def count_friends(self, radius):
        """Count the number of neighbors within a given radius (number of edges away). This is social relation and not spatial"""
        #Empty list, waterboard has no friends
        friends = []
        return len(friends)

    def step(self):
        #append past_flood_damages list with the new actual flood damage
        self.past_flood_damages.append(self.flood_damage_actual)

        #determine attitude of waterboard based upon past flood damages. The waterboard always has an attitude of at least 0.5
        self.waterboard_attitude = (5 + sum(self.past_flood_damages[-5:])) / 10


