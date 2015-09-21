import logging, glob, os, json, sys, collections

class Loader:
    def __init__(self, directoryPath):
        self.problemsDictionary = {}

        #allows for logging of messages during execution
        self.logger = logging.getLogger(__name__)

        #verifies that root directory contains problems directory
        problemsExists = False
        try:
            if "problems" in os.listdir(directoryPath):
            #builds initializing dictionary
                self.createProblemsDict(os.path.join(directoryPath, "problems"))
            else:
                self.logger.error("No problems directory was found!")
                sys.exit(1)
        except:
            self.logger.critical("No configuration directory found, see README.md: ")
            sys.exit(1)

    def createProblemsDict(self, path):
        meta_defaults = {}

        self.meta_defaults = self.metaDefaultsIn(os.path.join(path, "meta_defaults.json"))
        
        #finds subdirectories of problems dir and makes those the 
        #dictionary keys through passing them to the probStats function
        for problem in os.listdir(path):
            if (os.path.isdir(os.path.join(path,problem)) == True):
                self.probStats(path, problem, self.meta_defaults)

    def metaDefaultsIn(self, defaultPath):
        """Establishes meta default values by reading in from the meta-defaults.json"""
        defaults = {}
        
        with open(defaultPath) as f:
            defaults = json.load(f)
        return defaults

    def probStats(self, path, problem, meta_defaults):
        """Defines each problem and its attributes within the dictionary"""
        problemPath = os.path.join(path, problem)

        self.logger.info("Loading " + problem);
        self.problemsDictionary[problem] = {}

        #Puts description in the problemList
        with open(os.path.join(problemPath, "description.txt")) as desc:
            self.problemsDictionary[problem]["desc"] = desc.read()

        #Decides whether to use each meta value within the problem directory or
        #the default value if there is no value (null) for the dictionary value
        #and adds it to the problemList
        with open(os.path.join(problemPath, "meta.json")) as meta:
            tmpDict = json.load(meta)

        for key in meta_defaults.keys():
            if (tmpDict.get(key) == None):
                tmpDict[key] = meta_defaults[key]

        self.problemsDictionary[problem]["meta"] = tmpDict

        #Checks whether the input values exist and, if so, it adds it to the
        #problemList
        try:
            newPath = os.path.join(problemPath, "in.txt")
            open(newPath)
            self.problemsDictionary[problem]["in"] = newPath
        except:
            self.logger.warning("in.txt does not appear to exist.")

        #Add out.txt to problemList
        self.problemsDictionary[problem]["out"] = os.path.join(problemPath, "out.txt")

        #Return problem to be stored in the dictionary
        return

if __name__ == "__main__":
    import pprint
    print "Hello"
    logging.basicConfig(level=logging.DEBUG)
    loader = Loader("config")
    pprint.pprint(loader.problemsDictionary)
