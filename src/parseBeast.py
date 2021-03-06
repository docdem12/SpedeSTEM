import re, sys

DIVIDER = r'[\t ]+'
COLUMN_ONE = 'traits'
COLUMN_TWO = 'species'
COLUMN_THREE = 'groups'

class ParseBeast:
    ''' talk about 2 or 3 column file parsing'''

    def __init__ (self, settingsIn='settings', settingsOut='settings.stem', \
                  associations='associations.stem', theta=1.0):
        self.speciesToTraits = {}
        self.groupsToSpecies = {}
        self.header = ''

        assert settingsIn.strip() != settingsOut.strip(), \
            'Input settings file should not equal output settings file'

        try:
            settingsInFile = open(settingsIn, 'r')
            settingsOutFile = open(settingsOut, 'w')
        except IOError:
            print 'ERROR: Could not open beast formatted trait input and output files.'
            exit()

        self.buildHeader(theta)
        if self.doesIncludeAssociations(settingsInFile):
            print 'Parsing Beast traits file for Species, Traits, and Grouping'
            self.getSettingsAndAssociations(settingsInFile)

            try:
                associationsFile = open(associations, 'w')
            except IOError:
                print 'Could not open associations file for writing'
                exit()

            self.generateAssociations(associationsFile)

            associationsFile.close()
        else:
            print 'Parsing Beast traits file for Species and Traits only'
            self.getSettingsOnly(settingsInFile)
        self.generateSettings(settingsOutFile)

        try:
            settingsInFile.close()
            settingsOutFile.close()
        except IOError:
            print 'Trouble closing beast formatted trait input and output files.'
            exit()

    def getSettingsOnly(self, settingsFile):
        '''alters: self.speciesToTraits, format of file is "COL_ONE    COL_TWO" '''

        for line in settingsFile:
            splits = re.split(DIVIDER, line)
            if len(splits) != 2:
                print "BEAST ERROR: Could not parse Beast formatted settings file"
                sys.exit()
            species = splits[1].strip()
            if self.speciesToTraits.has_key(species):
                updatedTraits = self.speciesToTraits[species] + [splits[0].strip()]
                self.speciesToTraits[species] = updatedTraits
            else:
                self.speciesToTraits[species] = [splits[0].strip()]

    def getSettingsAndAssociations(self, settingsFile):
        '''alters: self.speciesToTraits, format of file is "COL_ONE    COL_TWO    COL_THREE" '''

        for line in settingsFile:
            splits = re.split(DIVIDER, line.strip())
            if len(splits) != 3:
                print "BEAST ERROR: Could not parse Beast formatted settings file"
                sys.exit()
            species = splits[1].strip()
            group = splits[2].strip()

            # build settings dict
            if self.speciesToTraits.has_key(species):
                updatedTraits = self.speciesToTraits[species] + [splits[0].strip()]
                self.speciesToTraits[species] = updatedTraits
            else:
                self.speciesToTraits[species] = [splits[0].strip()]

            # build associations dict
            if self.groupsToSpecies.has_key(group):
                previousSpecies = self.groupsToSpecies[group]
                if species not in previousSpecies:
                    updatedSpecies = previousSpecies + [species]
                    self.groupsToSpecies[group] = updatedSpecies
            else:
                self.groupsToSpecies[group] = [species]


    def doesIncludeAssociations(self, settingsFile):
        header = settingsFile.readline()
        parts = re.split(DIVIDER, header)

        if parts[0].strip().lower() != COLUMN_ONE:
            print 'BEAST ERROR: First column header must be traits keyword'
            sys.exit()
        if parts[1].strip().lower() != COLUMN_TWO:
            print'BEAST ERROR: Second column header must be species keyword'
            sys.exit()

        if len(parts) == 3:
            if parts[2].strip().lower() != COLUMN_THREE:
                print 'Third column header must be groups keyword'
                sys.exit()
            return True
        else:
            return False

    def buildHeader(self, theta):
        self.header = "properties:\n" + \
                        "\trun: 1\t\t\t#0=user-tree, 1=MLE, 2=search\n" + \
                        "\ttheta: " + str(theta) + "\n" + \
                        "\tnum_saved_trees: 15\n" + \
                        "\tbeta: 0.0005\n" + \
                        "species:\n"

    def generateSettings(self, settingsOutFile):
        ''' 
        Writes the settings file with speciesToTraits in the form of str to str.
        '''

        settingsOutFile.write(self.header)
        for name in self.speciesToTraits.keys() :
            settingsOutFile.write("\t" + name + ": ")
            counter = 1
            for trait in self.speciesToTraits[name]:
                if counter < len(self.speciesToTraits[name]):
                    settingsOutFile.write(trait + ", ")
                else:
                    settingsOutFile.write(trait + "\n")
                counter += 1

    def generateAssociations(self, associationsFile):
        ''' 
        Writes the associations file with groupsToSpecies in the form of str to str.
        '''

        for name in self.groupsToSpecies.keys() :
            associationsFile.write("\t" + name + ": ")
            counter = 1
            for trait in self.groupsToSpecies[name]:
                if counter < len(self.groupsToSpecies[name]):
                    associationsFile.write(trait + ", ")
                else:
                    associationsFile.write(trait + "\n")
                counter += 1

if __name__ == "__main__":
    tester = ParseBeast(theta=2.0)
    print tester.speciesToTraits

