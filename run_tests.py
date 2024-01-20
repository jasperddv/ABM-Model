import pandas as pd
from model import AdaptationModel
import matplotlib.pyplot as plt
import networkx as nx
from agents import Households, Government, Waterboard, Insurance_company, Policy_maker
from results_analysis import analyse_results
import random
import mesa

# set random seed
random.seed(1)

#0 if we want to run a single run, 1, 2, 3 or 4 if we want to run experiment for scenario experimentno
ScenarioNO = 4

#single run
if ScenarioNO == 0:
    # Initialize the Adaptation Model with 50 household agents.
    model = AdaptationModel(number_of_households=50, flood_map_choice="harvey", network="watts_strogatz") # flood_map_choice can be "harvey", "100yr", or "500yr"
    
    # Calculate positions of nodes for the network plot.
    # The spring_layout function positions nodes using a force-directed algorithm,
    # which helps visualize the structure of the social network.
    pos = nx.spring_layout(model.G)
    
    # Define a function to plot agents on the network.
    # This function takes a matplotlib axes object and the model as inputs.
    def plot_network(ax, model):
        # Clear the current axes.
        ax.clear()
        # Determine the color of each node (agent) based on their adaptation status.
        #This piece of code is an alternative for code below
        # colors = ['blue' if agent.is_adapted else 'red' for agent in model.schedule.agents]
        #to ensure that this piece of code is only executed for households
        colors = []
        for agent in model.schedule.agents:
            if type(agent) == Households:
                if agent.is_adapted:
                    colors.append('blue')
                else:
                    colors.append('red')
    
        # Draw the network with node colors and labels.
        nx.draw(model.G, pos, node_color=colors, with_labels=True, ax=ax)
        # Set the title of the plot with the current step number.
        ax.set_title(f"Social Network State at Step {model.schedule.steps}", fontsize=12)
    
    # Generate the initial plots at step 0.
    # Plot the spatial distribution of agents. This is a function written in the model.py
    model.plot_model_domain_with_agents()
    
    # Plot the initial state of the social network.
    fig, ax = plt.subplots(figsize=(7, 7))
    plot_network(ax, model)
    plt.show()

    # Run the model for 20 steps and generate plots every 5 steps.
    for step in range(20):
        model.step()

        # Every 5 steps, generate and display plots for both the spatial distribution and network.
        # Note the first step is step 0, so the plots will be generated at steps 4, 9, 14, and 19, which are the 5th, 10th, 15th, and 20th steps.
        if (step + 1) % 5 == 0:
            # Plot for the spatial map showing agent locations and adaptation status.
            plt.figure(figsize=(10, 6))
            model.plot_model_domain_with_agents()

            # Plot for the social network showing connections and adaptation statuses.
            fig, ax = plt.subplots(figsize=(7, 7))
            plot_network(ax, model)
            plt.show()

    agent_data = model.datacollector.get_agent_vars_dataframe()
    print(agent_data)

    model_data = model.datacollector.get_model_vars_dataframe()
    print(model_data)

#scenario 1
elif ScenarioNO == 1:
    # create experimental setup
    # start by creating dictionary for parameters
    experiment1_parameters = {'political_situation': [0.05, 0.95], 'scenarioNO': 1}


    # define function for experiment running
    def experimental_setup_1(flooding_model):
        batch = mesa.batchrunner.batch_run(model_cls=flooding_model, parameters=experiment1_parameters,
                                           number_processes=1, iterations=5, max_steps=19, data_collection_period=1,
                                           display_progress=True)
        # import data from run
        br_df = pd.DataFrame(batch)

        # export to CSV value, to be opened in Excel
        br_df.to_csv("Experimental_results")


    # run experimental setup
    experimental_setup_1(AdaptationModel)

#scenario 2
elif ScenarioNO == 2:
    # create experimental setup
    # start by creating dictionary for parameters
    experiment1_parameters = {'welfare': [0.05, 0.95], 'scenarioNO': 2}


    # define function for experiment running
    def experimental_setup_1(flooding_model):
        batch = mesa.batchrunner.batch_run(model_cls=flooding_model, parameters=experiment1_parameters,
                                           number_processes=1, iterations=5, max_steps=19, data_collection_period=1,
                                           display_progress=True)
        # import data from run
        br_df = pd.DataFrame(batch)

        # export to CSV value, to be opened in Excel
        br_df.to_csv("Experimental_results")


    # run experimental setup
    experimental_setup_1(AdaptationModel)

#scenario 3
elif ScenarioNO == 3:
    # create experimental setup
    # start by creating dictionary for parameters
    random_political_situation = random.random()
    experiment1_parameters = {"political_situation": random_political_situation, 'scenarioNO': [0, 3]}


    # define function for experiment running
    def experimental_setup_1(flooding_model):
        batch = mesa.batchrunner.batch_run(model_cls=flooding_model, parameters=experiment1_parameters,
                                           number_processes=1, iterations=5, max_steps=19, data_collection_period=1,
                                           display_progress=True)
        # import data from run
        br_df = pd.DataFrame(batch)

        # export to CSV value, to be opened in Excel
        br_df.to_csv("Experimental_results")


    # run experimental setup
    experimental_setup_1(AdaptationModel)

#scenario 4
elif ScenarioNO == 4:
    # create experimental setup
    # start by creating dictionary for parameters
    random_political_situation = random.random()
    experiment1_parameters = {"political_situation": random_political_situation, 'scenarioNO': [0, 4]}


    # define function for experiment running
    def experimental_setup_1(flooding_model):
        batch = mesa.batchrunner.batch_run(model_cls=flooding_model, parameters=experiment1_parameters,
                                           number_processes=1, iterations=5, max_steps=19, data_collection_period=1,
                                           display_progress=True)
        # import data from run
        br_df = pd.DataFrame(batch)

        # export to CSV value, to be opened in Excel
        br_df.to_csv("Experimental_results")


    # run experimental setup
    experimental_setup_1(AdaptationModel)

#default experimentation
else:
    # create experimental setup
    # start by creating dictionary for parameters
    random_political_situation = random.random()
    experiment1_parameters = {"political_situation" : random_political_situation}

    #define function for experiment running
    def experimental_setup_1(flooding_model):
        batch = mesa.batchrunner.batch_run(model_cls = flooding_model, parameters = experiment1_parameters,
                                           number_processes = 1, iterations = 5, max_steps = 19,data_collection_period = 1,
                                           display_progress=True)
        #import data from run
        br_df = pd.DataFrame(batch)

        #export to CSV value, to be opened in Excel
        br_df.to_csv("Experimental_results")


    # run experimental setup
    experimental_setup_1(AdaptationModel)

#show results in graphs for analysis
analyse_results(ScenarioNO)