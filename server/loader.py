import logging, glob, os, json, sys, collections

class Loader:
    def __init__(self, dataPath):
        #allows for logging of messages during execution
        self.logger = logging.getLogger(__name__)
        self.contests=self.initContests(dataPath)

    def initContests(self, path):
        contests = {}

        #Verify the config directory contains at least one contest
        contestExists=False
        if (len(os.listdir(path))>=1) and ("problems" not in os.listdir(path)):
            contestDirs = os.listdir(path)
            self.logger.debug("Found the following contest dirs: %s", contestDirs)

            #Drop hidden folders
            for dir in contestDirs:
                if dir[0] == '.':
                    self.logger.debug("Dropping hidden directory %s", dir)
                    contestDirs.remove(dir)

            #Iterate over remaining folders and create contests
            for contest in contestDirs:
                tempContest = {}
                tempContest["problems"] = self.loadContestProblems(os.path.join(path, contest))
                tempContest["languages"] = self.loadContestLanguages(os.path.join(path, contest))
                tempContest["users"] = self.loadContestUsers(os.path.join(path, contest))
                contests[contest] = tempContest
        else:
            self.logger.debug("Found only %s", os.listdir(path))

        return contests

    def loadContestUsers(self, contestDir):
        with open(os.path.join(contestDir, "passwd.json"), 'r') as f:
            users = json.load(f)
            self.logger.info("Loaded %s users for %s", len(users), contestDir)
            return users
    
    def loadContestLanguages(self, contestDir):
        with open(os.path.join(contestDir, "languages.json"), 'r') as f:
            langs = json.load(f)
            for lang in langs:
                self.logger.info("Loading Support for %s", langs[lang]["name"])
            return langs

    def loadContestProblems(self, contestDir):
        self.logger.info("Loading contest %s", contestDir)
        self.logger.debug("Entering %s, found %s", contestDir, os.listdir(contestDir))
        #verifies that contest directory contains problems directory
        problemsExists = False
        if "problems" in os.listdir(contestDir):
            #retrieve the problems for this contest
            problems = self.createProblemsDict(os.path.join(contestDir, "problems"))
        else:
            self.logger.error("No problems directory was found!")
            sys.exit(1)

        return problems

    def createProblemsDict(self, path):
        meta_defaults = {}
        problems = {}
        meta_defaults = self.metaDefaultsIn(os.path.join(path, "meta_defaults.json"))
        
        #finds subdirectories of problems dir and makes those the 
        #dictionary keys through passing them to the probStats function
        for problem in os.listdir(path):
            if (os.path.isdir(os.path.join(path,problem)) == True):
                problems[problem] = self.probStats(path, problem, meta_defaults)
        return problems
                
    def metaDefaultsIn(self, defaultPath):
        """Establishes meta default values by reading in from the meta-defaults.json"""
        defaults = {}
        
        with open(defaultPath) as f:
            defaults = json.load(f)
        return defaults

    def probStats(self, path, problem, meta_defaults):
        """Defines each problem and its attributes within the dictionary"""
        problemPath = os.path.join(path, problem)
        problemDict = {}
        self.logger.info("Loading " + problem);

        #Puts description in the problemList
        with open(os.path.join(problemPath, "description.txt")) as desc:
            problemDict["desc"] = desc.read()

        #Decides whether to use each meta value within the problem directory or
        #the default value if there is no value (null) for the dictionary value
        #and adds it to the problemList
        with open(os.path.join(problemPath, "meta.json")) as meta:
            tmpDict = json.load(meta)

        for key in meta_defaults.keys():
            if (tmpDict.get(key) == None):
                tmpDict[key] = meta_defaults[key]

        problemDict["meta"] = tmpDict

        #Checks whether the input values exist and, if so, it adds it to the
        #problemList
        try:
            newPath = os.path.join(problemPath, "in.txt")
            open(newPath)
            problemDict["in"] = newPath
        except:
            self.logger.warning("in.txt does not appear to exist.")

        #Add out.txt to problemList
        problemDict["out"] = os.path.join(problemPath, "out.txt")

        #Return problem to be stored in the dictionary
        return problemDict

if __name__ == "__main__":
    import pprint
    print "Hello"
    logging.basicConfig(level=logging.DEBUG)
    loader = Loader("config")
    pprint.pprint(loader.contests)
