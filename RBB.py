# Add to model class used
# here, the policy maker is called to determine the new value of provide_information
def provide_information(self):
    return self.policy_maker.provide_information

# here, the policy maker is called to determine the new value of subsidies
def subsidies(self):
    return self.policy_maker.subsidies

# here, the policy maker is called to determine the new value of regulation
def regulation(self):
    return self.policy_maker.regulation

# here, the policy maker is called to determine the new value of infrastructure government
def infrastructure_government(self):
    return self.policy_maker.infrastructure_government

# Add to list of agents
# Define the policy maker agent class
class Policy_maker(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

        # import all functions of the model to be able to use them in Insurance company
        self.main_model = model

        # initialise policy values
        self.provide_information = 0.5
        self.subsidies = 0.5
        self.regulation = 0.5
        self.infrastructure_government = 0.5

    # added this to ensure 'agent_metrics' works in model.py. Else FriendsCount does not work in the metrics
    def count_friends(self, radius):
        """Count the number of neighbors within a given radius (number of edges away). This is social relation and not spatial"""
        # Empty list, policy maker has no friends
        friends = []
        return len(friends)

    def determine_provide_information(self, provide_information, government_budget, political_perception_government,
                                      waterboard_attitude, protest):
        if self.main_model.scenarioNO == 4:
            return (
                        0.1 * government_budget + 0.3 * political_perception_government + 0.2 * waterboard_attitude + 0.1 * protest) / 0.7
        else:
            return (
                        provide_information + 0.1 * government_budget + 0.3 * political_perception_government + 0.2 * waterboard_attitude + 0.1 * protest) / 1.7

    def determine_subsidies(self, government_budget, subsidies, political_perception_government, waterboard_attitude,
                            protest):
        if self.main_model.scenarioNO == 4:
            return government_budget * (
                        0.3 * political_perception_government + 0.2 * waterboard_attitude + 0.1 * protest) / 2
        else:
            return government_budget * (
                        subsidies + 0.3 * political_perception_government + 0.2 * waterboard_attitude + 0.1 * protest) / 3

    def determine_regulation(self, regulation, government_budget, political_perception_government, waterboard_attitude,
                             protest):
        if self.main_model.scenarioNO == 4:
            return (
                        0.05 * government_budget + 0.2 * political_perception_government + 0.05 * waterboard_attitude + 0.1 * protest) / 0.4
        else:
            return (
                        regulation + 0.05 * government_budget + 0.2 * political_perception_government + 0.05 * waterboard_attitude + 0.1 * protest) / 1.4

    def determine_infrastructure_government(self, infrastructure_government, government_budget,
                                            political_perception_government, waterboard_attitude):
        if self.main_model.scenarioNO == 4:
            return (0.2 * government_budget + 0.3 * political_perception_government + 0.2 * waterboard_attitude) / 0.9
        else:
            return (
                        infrastructure_government + 0.2 * government_budget + 0.3 * political_perception_government + 0.2 * waterboard_attitude) / 1.9

    def step(self):
        # determine new policy values
        self.provide_information = self.determine_provide_information(self.provide_information,
                                                                      self.main_model.government.government_budget,
                                                                      self.main_model.government.political_perception_government,
                                                                      self.main_model.waterboard.waterboard_attitude,
                                                                      self.main_model.protest)
        self.subsidies = self.determine_subsidies(self.main_model.government.government_budget, self.subsidies,
                                                  self.main_model.government.political_perception_government,
                                                  self.main_model.waterboard.waterboard_attitude,
                                                  self.main_model.protest)
        self.regulation = self.determine_regulation(self.regulation, self.main_model.government.government_budget,
                                                    self.main_model.government.political_perception_government,
                                                    self.main_model.waterboard.waterboard_attitude,
                                                    self.main_model.protest)
        self.infrastructure_government = self.determine_infrastructure_government(self.infrastructure_government,
                                                                                  self.main_model.government.government_budget,
                                                                                  self.main_model.government.political_perception_government,
                                                                                  self.main_model.waterboard.waterboard_attitude)

    def advance(self):
        pass
