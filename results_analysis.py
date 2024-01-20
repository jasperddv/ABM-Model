import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def analyse_results(ScenarioNO):
    #read csv file and turn into pandas dataframe
    df = pd.read_csv("Experimental_results")

    #fill out current scenario number (should be the same for run_tests and results_analysis)
    ScenarioResultsNO = ScenarioNO

    #for scenario 1
    if ScenarioResultsNO == 1:
        #focus on households only
        Household_df = df.dropna()

        #create and plot sandbags placed by households boxplots
        sandbags_boxplot = sns.boxplot(data=Household_df, x="Step", y="SandbagsPlaced", hue="political_situation", fliersize = 0)
        sandbags_boxplot.set(ylim=(0, 4))
        plt.show()

        #create and plot households actual flood damages boxplots
        flooddamageactual_boxplot = sns.boxplot(data=Household_df, x="Step", y="FloodDamageActual", hue="political_situation", fliersize = 0)
        flooddamageactual_boxplot.set(ylim=(0, 1))
        plt.show()

        #create and plot infrastructure policy values scatterplot
        infrastructure_boxplot = sns.scatterplot(data=Household_df, x="Step", y="infrastructure_government", hue="political_situation")
        infrastructure_boxplot.set(ylim=(0, 1))
        plt.show()

        #create and plot subsidies policy values scatterplot
        subsidies_boxplot = sns.scatterplot(data=Household_df, x="Step", y="subsidies", hue="political_situation")
        subsidies_boxplot.set(ylim=(0,1))
        plt.show()

        #create and plot regulation policy values scatterplot
        regulation_boxplot = sns.scatterplot(data=Household_df, x="Step", y="regulation", hue="political_situation")
        regulation_boxplot.set(ylim=(0,1))
        plt.show()

        #create and plot provide information policy values scatterplot
        provide_information_boxplot = sns.scatterplot(data=Household_df, x="Step", y="provide_information", hue="political_situation")
        provide_information_boxplot.set(ylim=(0,1))
        plt.show()

    #for scenario 2
    if ScenarioResultsNO == 2:
        # focus on households only
        Household_df = df.dropna()

        #create and plot sandbags placed by households boxplots
        sandbags_boxplot = sns.boxplot(data=Household_df, x="Step", y="SandbagsPlaced", hue="welfare", fliersize = 0)
        sandbags_boxplot.set(ylim=(0, 4))
        plt.show()

        #create and plot households actual flood damages boxplots
        flooddamageactual_boxplot = sns.boxplot(data=Household_df, x="Step", y="FloodDamageActual", hue="welfare", fliersize = 0)
        flooddamageactual_boxplot.set(ylim=(0, 1))
        plt.show()

        #create and plot infrastructure policy values scatterplot
        infrastructure_boxplot = sns.scatterplot(data=Household_df, x="Step", y="infrastructure_government", hue="welfare")
        infrastructure_boxplot.set(ylim=(0, 1))
        plt.show()

        #create and plot subsidies policy values scatterplot
        subsidies_boxplot = sns.scatterplot(data=Household_df, x="Step", y="subsidies", hue="welfare")
        subsidies_boxplot.set(ylim=(0,1))
        plt.show()

        #create and plot regulation policy values scatterplot
        regulation_boxplot = sns.scatterplot(data=Household_df, x="Step", y="regulation", hue="welfare")
        regulation_boxplot.set(ylim=(0,1))
        plt.show()

        #create and plot provide information policy values scatterplot
        provide_information_boxplot = sns.scatterplot(data=Household_df, x="Step", y="provide_information", hue="welfare")
        provide_information_boxplot.set(ylim=(0,1))
        plt.show()

    #for scenario 3
    if ScenarioResultsNO == 3:
        # households only
        Household_df = df.dropna()

        # create separate dataframe for the new and old situation
        Household_new_sit_df = Household_df.loc[Household_df['scenarioNO'] == 3]
        Household_old_sit_df = Household_df.loc[Household_df['scenarioNO'] == 0]

        #create and plot sandbags placed by households boxplots for new situation
        newsit_sandbags_boxplot = sns.boxplot(data=Household_new_sit_df, x="Step", y="SandbagsPlaced", fliersize=0)
        newsit_sandbags_boxplot.set(ylim=(0, 4))
        plt.show()

        #create and plot sandbags placed by households boxplots for old situation
        oldsit_sandbags_boxplot = sns.boxplot(data=Household_old_sit_df, x="Step", y="SandbagsPlaced", fliersize=0)
        oldsit_sandbags_boxplot.set(ylim=(0, 4))
        plt.show()

        #create and plot households actual flood damages boxplots for new situation
        newsit_flooddamageactual_boxplot = sns.boxplot(data=Household_new_sit_df, x="Step", y="FloodDamageActual", fliersize=0)
        newsit_flooddamageactual_boxplot.set(ylim=(0, 1))
        plt.show()

        #create and plot households actual flood damages boxplots for old situation
        oldsit_flooddamageactual_boxplot = sns.boxplot(data=Household_old_sit_df, x="Step", y="FloodDamageActual", fliersize=0)
        oldsit_flooddamageactual_boxplot.set(ylim=(0, 1))
        plt.show()

        #create and plot infrastructure policy values scatterplot for new situation
        newsit_infrastructure_boxplot = sns.scatterplot(data=Household_new_sit_df, x="Step", y="infrastructure_government")
        newsit_infrastructure_boxplot.set(ylim=(0, 1))
        plt.show()

        #create and plot infrastructure policy values scatterplot for old situation
        oldsit_infrastructure_boxplot = sns.scatterplot(data=Household_old_sit_df, x="Step", y="infrastructure_government")
        oldsit_infrastructure_boxplot.set(ylim=(0, 1))
        plt.show()

        #create and plot subsidies policy values scatterplot for new situation
        newsit_subsidies_boxplot = sns.scatterplot(data=Household_new_sit_df, x="Step", y="subsidies")
        newsit_subsidies_boxplot.set(ylim=(0, 1))
        plt.show()

        #create and plot subsidies policy values scatterplot for old situation
        oldsit_subsidies_boxplot = sns.scatterplot(data=Household_old_sit_df, x="Step", y="subsidies")
        oldsit_subsidies_boxplot.set(ylim=(0, 1))
        plt.show()

        #create and plot regulation policy values scatterplot for new situation
        newsit_regulation_boxplot = sns.scatterplot(data=Household_new_sit_df, x="Step", y="regulation")
        newsit_regulation_boxplot.set(ylim=(0, 1))
        plt.show()

        #create and plot regulation policy values scatterplot for old situation
        oldsit_regulation_boxplot = sns.scatterplot(data=Household_old_sit_df, x="Step", y="regulation")
        oldsit_regulation_boxplot.set(ylim=(0, 1))
        plt.show()

        #create and plot provide information policy values scatterplot for new situation
        newsit_provide_information_boxplot = sns.scatterplot(data=Household_new_sit_df, x="Step", y="provide_information")
        newsit_provide_information_boxplot.set(ylim=(0, 1))
        plt.show()

        #create and plot provide information policy values scatterplot for old situation
        oldsit_provide_information_boxplot = sns.scatterplot(data=Household_old_sit_df, x="Step", y="provide_information")
        oldsit_provide_information_boxplot.set(ylim=(0, 1))
        plt.show()

    #for scenario 4
    if ScenarioResultsNO == 4:
        #households only
        Household_df = df.dropna()

        # create separate dataframe for the new and old situation
        Household_new_sit_df = Household_df.loc[Household_df['scenarioNO'] == 4]
        Household_old_sit_df = Household_df.loc[Household_df['scenarioNO'] == 0]

        #create and plot sandbags placed by households boxplots for new situation
        newsit_sandbags_boxplot = sns.boxplot(data=Household_new_sit_df, x="Step", y="SandbagsPlaced", fliersize=0)
        newsit_sandbags_boxplot.set(ylim=(0, 4))
        plt.show()

        #create and plot sandbags placed by households boxplots for old situation
        oldsit_sandbags_boxplot = sns.boxplot(data=Household_old_sit_df, x="Step", y="SandbagsPlaced", fliersize=0)
        oldsit_sandbags_boxplot.set(ylim=(0, 4))
        plt.show()

        #create and plot households actual flood damages boxplots for new situation
        newsit_flooddamageactual_boxplot = sns.boxplot(data=Household_new_sit_df, x="Step", y="FloodDamageActual", fliersize=0)
        newsit_flooddamageactual_boxplot.set(ylim=(0, 1))
        plt.show()

        #create and plot households actual flood damages boxplots for old situation
        oldsit_flooddamageactual_boxplot = sns.boxplot(data=Household_old_sit_df, x="Step", y="FloodDamageActual", fliersize=0)
        oldsit_flooddamageactual_boxplot.set(ylim=(0, 1))
        plt.show()

        #create and plot infrastructure policy values scatterplot for new situation
        newsit_infrastructure_boxplot = sns.scatterplot(data=Household_new_sit_df, x="Step", y="infrastructure_government")
        newsit_infrastructure_boxplot.set(ylim=(0, 1))
        plt.show()

        #create and plot infrastructure policy values scatterplot for old situation
        oldsit_infrastructure_boxplot = sns.scatterplot(data=Household_old_sit_df, x="Step", y="infrastructure_government")
        oldsit_infrastructure_boxplot.set(ylim=(0, 1))
        plt.show()

        #create and plot subsidies policy values scatterplot for new situation
        newsit_subsidies_boxplot = sns.scatterplot(data=Household_new_sit_df, x="Step", y="subsidies")
        newsit_subsidies_boxplot.set(ylim=(0, 1))
        plt.show()

        #create and plot subsidies policy values scatterplot for old situation
        oldsit_subsidies_boxplot = sns.scatterplot(data=Household_old_sit_df, x="Step", y="subsidies")
        oldsit_subsidies_boxplot.set(ylim=(0, 1))
        plt.show()

        #create and plot regulation policy values scatterplot for new situation
        newsit_regulation_boxplot = sns.scatterplot(data=Household_new_sit_df, x="Step", y="regulation")
        newsit_regulation_boxplot.set(ylim=(0, 1))
        plt.show()

        #create and plot regulation policy values scatterplot for old situation
        oldsit_regulation_boxplot = sns.scatterplot(data=Household_old_sit_df, x="Step", y="regulation")
        oldsit_regulation_boxplot.set(ylim=(0, 1))
        plt.show()

        #create and plot provide information policy values scatterplot for new situation
        newsit_provide_information_boxplot = sns.scatterplot(data=Household_new_sit_df, x="Step", y="provide_information")
        newsit_provide_information_boxplot.set(ylim=(0, 1))
        plt.show()

        #create and plot provide information policy values scatterplot for old situation
        oldsit_provide_information_boxplot = sns.scatterplot(data=Household_old_sit_df, x="Step", y="provide_information")
        oldsit_provide_information_boxplot.set(ylim=(0, 1))
        plt.show()