from collections import defaultdict
import re



class TexHelper(object):
    @staticmethod
    def composeOptions(texOptions):
        optionsString = '['
        for option, value in texOptions.iteritems():
            optionsString += str(option)
            if value is not None:
                optionsString += '=%s' % str(value)
            optionsString += ','
        optionsString += ']'
        return optionsString.replace(',]', ']')

    @staticmethod
    def createIndentString(nIndent):
        return ' ' * int(nIndent)

    @staticmethod
    def indentEachLineInString(nIndent, string):
        return '\n'.join(re.sub('^', '%s' % TexHelper.createIndentString(nIndent), x) for x in string.split('\n'))

    @staticmethod
    def createImageNodeString(filename, nodeIndex, options, basename):
        options['inner sep'] = 0
        return '\\node%s (%s%s) {\includegraphics[width=\\textwidth]{%s}};' % (TexHelper.composeOptions(options),
                                                                               basename,
                                                                               str(nodeIndex),
                                                                               str(filename))

    @staticmethod
    def createLayerString(layerList):
        resultString = ''
        for layer in layerList.split(','):
            if layer == 'background' or layer == 'main':
                continue
            resultString += '\\pgfdeclarelayer{%s}\n' % layer
        resultString += '\\pgfsetlayers{%s}\n' % layerList
        return resultString


    @staticmethod
    def createPackagesString(packagesList):
        resultString = ''
        for options, package in packagesList:
            resultString += '\usepackage[%s]{%s}\n' % (options, package)
        return resultString


    @staticmethod
    def createTikzlibrariesString(librariesList):
        resultString = ''
        for library in librariesList.split(','):
            resultString += '\usetikzlibrary{%s}\n' % library
        return resultString


class TexObject(object):
    def __init__(self, texOptions):
        self.texOptions = texOptions

    def toString(self):
        return self._composeString()
    
    def _composeString(self):
        return ''
    

class TexMaster(TexObject):
    def __init__(self,
                 completeScope,
                 fieldOfViewScope,
                 overlayScope,
                 texOptions
                 ):
        super(TexMaster, self).__init__(texOptions)
        self.completeScope = completeScope
        self.fieldOfViewScope = fieldOfViewScope
        self.overlayScope = overlayScope

    

    def _composeString(self):
        optionsString = self._composeOptions()
        initialIndent = TexHelper.createIndentString(int(self.texOptions['indent']))
        firstIndent = TexHelper.createIndentString(int(self.texOptions['indent']) + int(self.texOptions['indentStep']))
        secondIndent = int(self.texOptions['indent']) + 2*int(self.texOptions['indentStep'])
        composition = """%s\\resizebox{%s}{!}{
%s\\begin{tikzpicture}%s
%s
%s
%s
%s\\end{tikzpicture}
%s}""" % (initialIndent,
          self.texOptions['scale'],
          firstIndent,
          optionsString,
          TexHelper.indentEachLineInString(secondIndent, self.completeScope.toString()),
          TexHelper.indentEachLineInString(secondIndent, self.fieldOfViewScope.toString()),
          TexHelper.indentEachLineInString(secondIndent, self.overlayScope.toString()),
          firstIndent,
          initialIndent
)
        return composition


    def _composeOptions(self):
        return TexHelper.composeOptions(self.texOptions['tikzpicture'])


class TexCompleteScope(TexObject):
    def __init__(self, scopeOptions):
        super(TexCompleteScope, self).__init__(scopeOptions)

    def _composeString(self):
        optionsString = TexHelper.composeOptions(self.texOptions['scope']['options'])
        currIndent = 0
        indentStep = int(self.texOptions['indentStep'])
        composition = '\\begin{pgfonlayer}{%s}\n' % self.texOptions['layer']
        currIndent += indentStep

        composition += '%s\\begin{scope}%s\n' % (TexHelper.createIndentString(currIndent), optionsString)
        
        scopeString = ''
        currIndent += indentStep
        indentString = TexHelper.createIndentString(currIndent)

        imageDict = self.texOptions['images']
        imageKeys = [x[0] for x in sorted(imageDict.iteritems(), key=lambda y: int(y[1]['index']))]
        imageDict[imageKeys[0]]['options']['anchor'] = 'south west'
        if len(imageKeys) > 0:
            scopeString += indentString + TexHelper.createImageNodeString(imageKeys[0],
                                                                          imageDict[imageKeys[0]]['index'],
                                                                          imageDict[imageKeys[0]]['options'],
                                                                          self.texOptions['nodeNameBase']) + '\n'
        for idx, key in enumerate(imageKeys):
            if idx == 0:
                continue
            # imageDict[key]['options']['xshift'] =  
            # '($(%s)-(%s)$)' % (imageDict[key]['nodeName'], imageDict[imageKeys[0]]['nodeName']) use this for later stuff
            scopeString += indentString + \
                TexHelper.createImageNodeString(key,
                                                imageDict[key]['index'],
                                                imageDict[key]['options'],
                                                self.texOptions['nodeNameBase']) + \
                 '\n'
        composition += scopeString
        currIndent -= indentStep

        composition += '%s\\end{scope}\n' % (TexHelper.createIndentString(currIndent))

        currIndent -= indentStep

        composition += '\\end{pgfonlayer}'

        composition += '''

\\coordinate (width1) at ($(%s.east)-(%s.west)$);
\\ExtractCoordinate{width1}
\\setlength{\\firstscope}{\\XCoord}
''' % (imageDict[imageKeys[-1]]['nodeName'], imageDict[imageKeys[0]]['nodeName'])
    

        return composition


class TexFieldOfViewScope(TexObject):
    def __init__(self, scopeOptions):
        super(TexFieldOfViewScope, self).__init__(scopeOptions)

    def _composeString(self):
        # get fake scope first
        scopeOptions = dict(self.texOptions['scope']['options'])
        scopeOptions['opacity'] = '0.0'
        scopeOptions['overlay'] = None
        optionsString = TexHelper.composeOptions(scopeOptions)
        currIndent = 0
        indentStep = self.texOptions['indentStep']
        composition = '\\begin{pgfonlayer}{%s}\n' % 'background'
        currIndent += indentStep

        composition += '%% fake scope \n %s\\begin{scope}%s\n' % (TexHelper.createIndentString(currIndent), optionsString)
        currIndent += indentStep

        scopeString = ''
        indentString = TexHelper.createIndentString(currIndent)

        imageDict = self.texOptions['fakes']
        imageKeys = [x[0] for x in sorted(imageDict.iteritems(), key=lambda y: int(y[1]['index']))]

        imageDict[imageKeys[0]]['options']['anchor'] = 'south west'
        if len(imageKeys) > 0:
            scopeString += indentString + TexHelper.createImageNodeString(imageKeys[0],
                                                                          imageDict[imageKeys[0]]['index'],
                                                                          imageDict[imageKeys[0]]['options'],
                                                                          self.texOptions['fakeNameBase']) + '\n'
        for idx, key in enumerate(imageKeys):
            if idx == 0:
                continue
            scopeString += indentString + \
              TexHelper.createImageNodeString(key,
                                              imageDict[key]['index'],
                                              imageDict[key]['options'],
                                              self.texOptions['fakeNameBase']) + \
              '\n'
        composition += scopeString
        currIndent -= indentStep
        composition += '%s\\end{scope}\n' % TexHelper.createIndentString(currIndent)
        
        currIndent -= indentStep

        composition += '\\end{pgfonlayer}'

        composition += '''

\\coordinate (width2) at ($(%s.east)-(%s.west)$);
\\ExtractCoordinate{width2}
\\setlength{\\secondscope}{\\XCoord}
\\pgfmathsetmacro{\\ratio}{\\firstscope/\\secondscope}

''' % (imageDict[imageKeys[-1]]['nodeName'], imageDict[imageKeys[0]]['nodeName'])

        # get real scope
        scopeOptions = self.texOptions['scope']['options']
        scopeOptions['scale'] = '\\ratio'
        optionsString = TexHelper.composeOptions(scopeOptions)
        currIndent = 0
        indentStep = self.texOptions['indentStep']
        composition += '\\begin{pgfonlayer}{%s}\n ' % self.texOptions['layer']
        currIndent += indentStep

        composition += '%% real scope \n %s\\begin{scope}%s\n' % (TexHelper.createIndentString(currIndent), optionsString)

        currIndent += indentStep

        scopeString = ''
        indentString = TexHelper.createIndentString(currIndent)

        imageDict = self.texOptions['images']
        imageKeys = [x[0] for x in sorted(imageDict.iteritems(), key=lambda y: int(y[1]['index']))]

        if len(imageKeys) > 0:
            imageDict[imageKeys[0]]['options']['anchor'] = 'south west'
            imageDict[imageKeys[0]]['options']['transform shape'] = None
            scopeString += indentString + TexHelper.createImageNodeString(imageKeys[0],
                                                                          imageDict[imageKeys[0]]['index'],
                                                                          imageDict[imageKeys[0]]['options'],
                                                                          self.texOptions['nodeNameBase']) + '\n'

        for idx, key in enumerate(imageKeys):
            if idx == 0:
                continue
            imageDict[key]['options']['transform shape'] = None
            scopeString += indentString + \
              TexHelper.createImageNodeString(key,
                                              imageDict[key]['index'],
                                              imageDict[key]['options'],
                                              self.texOptions['nodeNameBase']) + \
              '\n'
        composition += scopeString
        currIndent -= indentStep
        composition += '%s\\end{scope}\n' % TexHelper.createIndentString(currIndent)
                                                                          
        currIndent -= indentStep

        composition += '\\end{pgfonlayer}\n'

        return composition


class TexStandaloneDecorator(TexObject):
    def __init__(self, texMaster, options):
        super(TexStandaloneDecorator, self).__init__(options)
        self.texMaster = texMaster

    def _composeString(self):
        res_string = '''\documentclass{standalone}

%s
%s
%s
\\newdimen\\XCoord
\\newdimen\\YCoord
\\newcommand*{\\ExtractCoordinate}[1]{\\path (#1); \\pgfgetlastxy{\\XCoord}{\\YCoord};}%%

\\newlength{\\firstscope}
\\newlength{\\secondscope}

\\begin{document}

%s
\\end{document}''' % (TexHelper.createPackagesString(self.texOptions['packages']),
                     TexHelper.createTikzlibrariesString(self.texOptions['tikzlibraries']),
                     TexHelper.createLayerString(self.texOptions['layers']),
                     texMaster.toString())
        return res_string
        



if __name__ == "__main__":
    import copy
    import FileComprehension
    texDefaultOptions = FileComprehension.TexDefaultOptions()
    userOptions = {}
    parsedOptions = FileComprehension.OptionParser.parse(texDefaultOptions.mergeUserOptions(userOptions))
    
    # options = defaultdict(dict, {
    #     'tikzpicture' :
    #     {
    #         'a' : 1, 'b' : None
    #     },
    #     'indent' : 0,
    #     'indentStep' : 4,
    #     'images' :
    #     {
    #         'a' :
    #         {
    #             'index' : 0, 'options' : {}, 'nodeName' : 'zig', 'nodeNameBase' : 'WUUUZA', 'fakeNameBase' : 'gefakt'
    #         },
    #         'b' :
    #         {
    #             'index':1, 'options' : {'xshift' : '50'}, 'nodeName' : 'mizzge', 'nodeNameBase' : 'BAAAAZE', 'fakeNameBase' : 'gefukt'
    #         }
    #     },
    #     'xshift' : '10',
    #     'scale' : 1.0,
    #     'layer' : 'blalayer'})
    texMaster = TexMaster(TexCompleteScope(parsedOptions['completeScope']),
                          TexFieldOfViewScope(parsedOptions['fieldOfViewScope']),
                          TexObject(parsedOptions['overlay']),
                          parsedOptions['general']
                          )
    standalone = TexStandaloneDecorator(texMaster, parsedOptions['general'])

    print standalone.toString()
