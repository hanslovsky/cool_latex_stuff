from collections import defaultdict
import re
import copy



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


class TexEnvironmentCreator(object):
    @staticmethod
    def begin(environment, additionalString):
        return '\\begin{%s}%s' % (environment, additionalString)

    @staticmethod
    def end(environment):
        return '\\end{%s}' % environment

    def __init__(self, environmentCreators, environmentContent):
        self.innerEnvironments = environmentCreators
        self.content = environmentContent

    def getEnvironment(self):
        return self.content % tuple(x.getEnvironment() for x in self.innerEnvironments)



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

        scopeNodes = []

        imageDict = self.texOptions['images']
        imageKeys = [x[0] for x in sorted(imageDict.iteritems(), key=lambda y: int(y[1]['index']))]
        imageDict[imageKeys[0]]['options']['anchor'] = 'south west'
        if len(imageKeys) > 0:
            scopeString += indentString + TexHelper.createImageNodeString(imageKeys[0],
                                                                          imageDict[imageKeys[0]]['index'],
                                                                          imageDict[imageKeys[0]]['options'],
                                                                          self.texOptions['nodeNameBase']) + '\n'
        for idx, key in enumerate(imageKeys):
            scopeNodes.append(imageDict[key]['nodeName'])
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

        composition += '''
\\node[inner sep=0, fit=%s] (completeScopeHelper) {};
''' % ' '.join('(%s)' % x  for x in scopeNodes)
    

        return composition


class TexFieldOfViewScope(TexObject):
    def __init__(self, scopeOptions):
        super(TexFieldOfViewScope, self).__init__(scopeOptions)

    def _putLinesToEnvironment(self, group, values, typeId, indentIndex):
        scale = False
        indents = [TexHelper.createIndentString(x*int(self.texOptions['indentStep'])) for x in xrange(indentIndex+2+1)]
        values = copy.deepcopy(values)
        if typeId == 'fakes':
            values['layer'] = 'background'
            values['scopeOptions']['scale'] = 1.0
            values['scopeOptions']['overlay'] = None
            values['scopeOptions']['opacity'] = 0.0
            nodeNameBase = self.texOptions['fakeNameBase']
        else:
            nodeNameBase = self.texOptions['nodeNameBase']
            if values['scale']:
                values['scopeOptions']['scale'] = '\\ratio'
                scale = True

        contentString = ''
        for idx, (imageKey, image) in enumerate(sorted(values[typeId].iteritems(), key=lambda x: x[1]['index'])):
            if idx == 0:
                image['options']['anchor'] = 'south west'
            if scale:
                image['options']['transform shape'] = None
            contentString += indents[indentIndex + 2]
            contentString += TexHelper.createImageNodeString(imageKey,
                                                             image['index'],
                                                             image['options'],
                                                             nodeNameBase) + '\n'

        pgfOnLayerString  = '\n%s%s\n' % (indents[indentIndex],
                                          TexEnvironmentCreator.begin('pgfonlayer', '{%s}' % values['layer']))
        pgfOnLayerString += '%s\n'
        pgfOnLayerString += '%s%s\n' % (indents[indentIndex],
                                      TexEnvironmentCreator.end('pgfonlayer'))

        allNodes = ' '.join(('(%s)' % x[1]['nodeName'] for x in values[typeId].iteritems()))
        if typeId == 'fakes':
           pgfOnLayerString += '\\node[inner sep = 0, fit=%s] (fakeFit) {};\n' % allNodes
           pgfOnLayerString += '''
\\coordinate (width2) at ($(fakeFit.east)-(fakeFit.west)$);
\\ExtractCoordinate{width2}
\\setlength{\\secondscope}{\\XCoord}
\\pgfmathsetmacro{\\ratio}{\\firstscope/\\secondscope}
\\pgfresetboundingbox
'''

        scopeString  = '\n%s%s\n' % (indents[indentIndex+1],
                                     TexEnvironmentCreator.begin('scope', TexHelper.composeOptions(values['scopeOptions'])))
        scopeString += '%s\n'
        
        
        scopeString += '%s%s\n' %  (indents[indentIndex+1],
                                    TexEnvironmentCreator.end('scope'))

        scopeEnvironment = TexEnvironmentCreator([TexEnvironmentCreator([], contentString)], scopeString)
        return TexEnvironmentCreator([scopeEnvironment], pgfOnLayerString)




    def _composeString(self):
        # get fake scope first

        containedNodes = []
        contentEnvironments = []
        
        for group, values in self.texOptions['lines'].iteritems():
            if values['scale']:
                contentEnvironments.append(self._putLinesToEnvironment(group, values, 'fakes', 1))
            contentEnvironments.append(self._putLinesToEnvironment(group, values, 'images', 1))
            containedNodes += (x[1]['nodeName'] for x in values['images'].iteritems())

        scopeOptions = dict(self.texOptions['scope']['options'])
        indents = [TexHelper.createIndentString(x*int(self.texOptions['indentStep'])) for x in xrange(5)]
        optionsString = TexHelper.composeOptions(scopeOptions)
        scopeString  = '\n%s\n' % TexEnvironmentCreator.begin('scope', optionsString)
        scopeString += '%s\n' % ('\n'.join(['%s'] * len(contentEnvironments)))
        scopeString += '\\node[fit=%s, inner sep=0] (fovFit) {};\n' % ' '.join('(%s)' % x for x in containedNodes)
        scopeString += '\\node[fit=(completeScopeHelper), inner sep=0] {};\n'
        scopeString += '%s\n' % TexEnvironmentCreator.end('scope')
            
        return TexEnvironmentCreator(contentEnvironments, scopeString).getEnvironment()

        

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


class TexOverlayScope(TexObject):
    _correspondences = {(2, 'SouthWest', 'SouthEast') : ('south west', 'south east'),
                        (3, 'SouthEast', 'NorthEast') : ('south east', 'north east'),
                        (4, 'NorthEast', 'NorthWest') : ('north east', 'north west'),
                        (1, 'NorthWest', 'SouthWest') : ('north west', 'south west')
                        }

    def __init__(self, options):
        super(TexOverlayScope, self).__init__(options)

    def _composeString(self):
        resString  = self._createIndicators() + '\n'
        resString += self._createFrames() + '\n'
        resString += self._createConnectors() + '\n'
        return resString

    def _createIndicators(self):
        scopeEnvironments = []
        # relPos = self.texOptions['relativeIndicatorPosition']
        # relRes = self.texOptions['relativeIndicatorResolution']
        for pair, values in self.texOptions['pairs'].iteritems():
            relPos = values['relativeIndicatorPosition']
            relRes = values['relativeIndicatorResolution']
            coordinates = {}
            coordinates['SouthWest'] = (min(relPos[0], relPos[0] + relRes[0]), min(relPos[1], relPos[1] + relRes[1]))
            coordinates['SouthEast'] = (max(relPos[0], relPos[0] + relRes[0]), min(relPos[1], relPos[1] + relRes[1]))
            coordinates['NorthEast'] = (max(relPos[0], relPos[0] + relRes[0]), max(relPos[1], relPos[1] + relRes[1]))
            coordinates['NorthWest'] = (min(relPos[0], relPos[0] + relRes[0]), max(relPos[1], relPos[1] + relRes[1]))
            coordinateString = ''
            for key, value in coordinates.iteritems():
                coordinateString += '''%s\\coordinate (%s%s%s) at ($(%s.south west)+%s$);\n
''' % (TexHelper.createIndentString(2*self.texOptions['indentStep']),
       self.texOptions['indicatorNameBase'],
       key,
       pair[2],
       values['nodeFrom'],
       value)
            scopeOptions = dict(self.texOptions['scope']['options'])
            scopeOptions['x'] = '($(%s.south east)-(%s.south west)$)' % (values['nodeFrom'], values['nodeFrom'])
            scopeOptions['y'] = '($(%s.north west)-(%s.south west)$)' % (values['nodeFrom'], values['nodeFrom'])
            scopeString = '''
%s%s
%s\\draw%s ($%s+(%s.south west)$) rectangle ($%s+(%s.south west)$);
%s
%s%s
''' % (TexHelper.createIndentString(self.texOptions['indentStep']),
       TexEnvironmentCreator.begin('scope', TexHelper.composeOptions(scopeOptions)),
       TexHelper.createIndentString(2*self.texOptions['indentStep']),
       TexHelper.composeOptions(values['indicatorOptions']),
       relPos,
       values['nodeFrom'],
       (relPos[0] + relRes[0], relPos[1] + relRes[1]),
       values['nodeFrom'],
       coordinateString,
       TexHelper.createIndentString(self.texOptions['indentStep']),
       TexEnvironmentCreator.end('scope'))

            scopeEnvironments.append(TexEnvironmentCreator([], scopeString))
            

        pgfLayerString  = '%s\n' % TexEnvironmentCreator.begin('pgfonlayer', '{%s}' % self.texOptions['indicatorLayer'])
        pgfLayerString += '\n'.join(['%s'] * len(scopeEnvironments)) + '\n'
        pgfLayerString += '%s\n' % TexEnvironmentCreator.end('pgfonlayer')
        pgfLayer = TexEnvironmentCreator(scopeEnvironments, pgfLayerString)
            
        return pgfLayer.getEnvironment()

    def _createFrames(self):
        scopeEnvironments = []
        scopeString = '\n'
        for pair, values in self.texOptions['pairs'].iteritems():
            values['frameOptions']['fit'] = '(%s)' % values['nodeTo']
            scopeString += '%s\\node%s (%s%s) {};\n' % (TexHelper.createIndentString(2*self.texOptions['indentStep']),
                                                        TexHelper.composeOptions(values['frameOptions']),
                                                        self.texOptions['frameNameBase'],
                                                        pair[1])
        scopeEnvironmentString = '''     
%s%s
%s
%s%s
''' % (TexHelper.createIndentString(self.texOptions['indentStep']),
       TexEnvironmentCreator.begin('scope', TexHelper.composeOptions(self.texOptions['scope']['options'])),     
       '%s',
       TexHelper.createIndentString(self.texOptions['indentStep']),
       TexEnvironmentCreator.end('scope'))
        scopeEnvironments.append(TexEnvironmentCreator([TexEnvironmentCreator([], scopeString)], scopeEnvironmentString))
        layerEnvironmentString = '''
%s
%s
%s
''' % (TexEnvironmentCreator.begin('pgfonlayer', '{%s}' % self.texOptions['frameLayer']),
       '%s',
       TexEnvironmentCreator.end('pgfonlayer'))

        return TexEnvironmentCreator(scopeEnvironments, layerEnvironmentString).getEnvironment()
        

    def _createConnectors(self):
        connectorString = ''
        for pair, values in self.texOptions['pairs'].iteritems():
            for indicator, frame in sorted(TexOverlayScope._correspondences.iteritems(), key=lambda x: x[0][0]):
                connectorString += '''%s\path%s (%s%s%s) to[bend left=%s] (%s%s.%s) to (%s%s.%s) to[bend right=%s] (%s%s%s);
''' % (TexHelper.createIndentString(2*self.texOptions['indentStep']),
       TexHelper.composeOptions(values['connectorOptions']['options']),
       self.texOptions['indicatorNameBase'],
       indicator[1],
       pair[2],
       values['connectorOptions']['bend'],
       self.texOptions['frameNameBase'],
       pair[1],
       frame[0],
       self.texOptions['frameNameBase'],
       pair[1],
       frame[1],
       values['connectorOptions']['bend'],
       self.texOptions['indicatorNameBase'],
       indicator[2],
       pair[2])

        scopeString  = TexHelper.createIndentString(self.texOptions['indentStep'])
        scopeString += TexEnvironmentCreator.begin('scope', TexHelper.composeOptions(self.texOptions['scope']['options']))
        scopeString += '\n%s\n'
        scopeString += TexHelper.createIndentString(self.texOptions['indentStep'])
        scopeString += TexEnvironmentCreator.end('scope') + '\n'

        pgfLayerString  = TexEnvironmentCreator.begin('pgfonlayer', '{%s}' % self.texOptions['connectorLayer']) + '\n'
        pgfLayerString += '\n%s\n'
        pgfLayerString += TexEnvironmentCreator.end('pgfonlayer') + '\n'

        scope = [TexEnvironmentCreator([TexEnvironmentCreator([], connectorString)], scopeString)]

        return TexEnvironmentCreator(scope, pgfLayerString).getEnvironment()




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
                          TexOverlayScope(parsedOptions['overlay']),
                          parsedOptions['general']
                          )
    standalone = TexStandaloneDecorator(texMaster, parsedOptions['general'])

    print standalone.toString()
