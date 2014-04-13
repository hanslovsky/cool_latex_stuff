import xmldict # pip install xmldict
import json # built-in
import types # built-in
import copy

class TexDefaultOptions(object):
    defaultOptions = {'general' : {
        'indent' : 0,
        'indentStep' : 4,
        'tikzpicture' : {
            'framed' : None,
            'background rectangle/.style' : '{thin, top color=black!80, bottom color=black!0}'
        },
        'scale' : '1.0\\linewidth',
        'packages' : [('','tikz'), ('', 'pgf')],
        'tikzlibraries' : 'fit,calc,positioning,backgrounds',
        'layers' : 'background,lower,upper,main'
    },
    'completeScope' : {
        'layer' : 'lower',
        'scope' : {
            'options' : {
                'opacity' : 1.0
            }
        },
        'images' : {
            'example_images/arnie.jpg' : {
                'index' : 1, 'options' : {}
            },
            'example_images/arnie2.jpg' : {
                'index' : 2, 'options' : {}
            }
        },
        'nodeNameBase' : 'completeView',
        'options' : {},
    },
    'fieldOfViewScope' : {
        'layer' : 'upper',
        'options' : {},
        'scope' : {
            'options' : {
                'opacity' : 1.0,
                'yshift' : '-10cm'
            }
        },
        'lines' : {
            1 : {
                'options' : {},
                'images' : {
                    'example_images/arnie.jpg' : {
                        'index' : 1, 'options' : {}
                    },
                    'example_images/arnie2.jpg' : {
                        'index' : 2, 'options' : {}
                    },
                    'example_images/arnie3.jpg' : {
                        'index' : 3, 'options' : {}
                    },
                    'example_images/arnie4.jpg' : {
                        'index' : 4, 'options' : {}
                    }
                }
            }
        },
        'fakeNameBase' : 'fake',
        'nodeNameBase' : 'fieldOfView',
    },
    'overlay' : {
        'scope' : {
            'options' : {
                'overlay' : None
            }
        },
        'options' : {
            'opacity' : 0.3,
            'color' : 'red!30'
        },
        'pairs' : {
            (1,1) : { 'frameOptions' : {}, 'connectorOptions' : {}},
            (2,4) : { 'frameOptions' : {}, 'connectorOptions' : {}}
        },
        'bend' : 0,
        'indicatorNameBase' : 'indicator',
        'frameNameBase' : 'frame'
    }
    }
        

    def __init__(self):
        pass

    def mergeUserOptions(self, userOptions):
        mergedDict = dict(TexDefaultOptions.defaultOptions)
        TexDefaultOptions.merge(userOptions, mergedDict)
        return mergedDict

    @staticmethod
    def merge(first, second):
        for key, value in first.iteritems():
            if type(value) is types.DictType:
                if not second.has_key(key):
                    second[key] = dict(value)
                else:
                    TexDefaultOptions.merge(value, second[key])
            else:
                second[key] = value
                


class ToDictConverter(object):
    def convert(self):
        return TexDefaultOptions.defaultOptions


class JsonToDictConverter(ToDictConverter):
    def __init__(self, filename):
        super(JsonToDictConverter, this).__init__()
        self.filename = filename

    def convert(self):
        return json.load(open(self.filename))


class XmlToDictConverter(ToDictConverter):
    def __init__(self, filename):
        super(JsonToDictConverter, this).__init__()
        self.filename = filename

    def convert(self):
        return xmldict.dict_to_xml(open(self.filename))


class OptionParser(object):
    @staticmethod
    def parse(options):
        OptionParser.addGlobalOptionsToLocal(options['general'], options['completeScope'])
        OptionParser.addGlobalOptionsToLocal(options['general'], options['fieldOfViewScope'])
        OptionParser.addGlobalOptionsToLocal(options['general'], options['overlay'])
        completeScopeOptions = options['completeScope']
        OptionParser.parseCompleteScopeOptions(completeScopeOptions)
        fieldOfViewScopeOptions = options['fieldOfViewScope']
        OptionParser.parseFieldOfViewScopeOptions(fieldOfViewScopeOptions)
        overlayOptions = options['overlay']
        OptionParser.parseOverlayOptions(overlayOptions, completeScopeOptions['images'], fieldOfViewScopeOptions['images'])

        return options

    @staticmethod
    def parseCompleteScopeOptions(completeScopeOptions):
        images = completeScopeOptions['images']
        prevKey = -1
        for image, options in sorted(images.iteritems(), key=lambda x: int(x[1]['index'])):
            options['nodeName'] = completeScopeOptions['nodeNameBase'] + str(options['index'])
            generalImageOptions = dict(completeScopeOptions['options'])
            TexDefaultOptions.merge(options['options'], generalImageOptions)
            options['options'] = generalImageOptions
            if prevKey > -1:
                options['options']['right'] = 'of %s%d' % (completeScopeOptions['nodeNameBase'], prevKey)
            prevKey = int(options['index'])
            

    @staticmethod
    def parseFieldOfViewScopeOptions(fieldOfViewScopeOptions):
        keyValuePairs = []
        fakeKeyValuePairs = []
        for idx, (line, lineContent) in enumerate(sorted(fieldOfViewScopeOptions['lines'].iteritems(),
                                                         key=lambda x: int(x[0]))):
            generalLineOptions = dict(fieldOfViewScopeOptions['options'])
            TexDefaultOptions.merge(lineContent['options'], generalLineOptions)
            lineContent['options'] = generalLineOptions
            images = lineContent['images']
            prevKey = -1
            for image, options in sorted(images.iteritems(), key=lambda x: int(x[1]['index'])):
                options['nodeName'] = fieldOfViewScopeOptions['nodeNameBase'] + str(options['index'])
                generalImageOptions = dict(lineContent['options'])
                TexDefaultOptions.merge(options['options'], generalImageOptions)
                options['options'] = generalImageOptions
                if prevKey > -1:
                    options['options']['right'] = 'of %s%d' % (fieldOfViewScopeOptions['nodeNameBase'], prevKey)
                if idx == 0:
                    fakeOptions = copy.deepcopy(options)
                    fakeOptions['nodeName'] = fieldOfViewScopeOptions['fakeNameBase'] + str(options['index'])
                    if prevKey > -1:
                        fakeOptions['options']['right'] = 'of %s%d' % (fieldOfViewScopeOptions['fakeNameBase'], prevKey)
                    fakeKeyValuePairs.append((image, fakeOptions))
                keyValuePairs.append((image, options))
                prevKey = int(options['index'])
        fieldOfViewScopeOptions['images'] = {}
        fieldOfViewScopeOptions['fakes']  = {}
        for key, value in keyValuePairs:
            fieldOfViewScopeOptions['images'][key] = value
        for key, value in fakeKeyValuePairs:
            fieldOfViewScopeOptions['fakes'][key] = value


    @staticmethod
    def parseOverlayOptions(overlayOptions, completeScopeImages, fieldOfViewImages):
        pairs = overlayOptions['pairs']
        for idx, (pair, options) in enumerate(pairs.iteritems()):
            generalPairOptions = dict(overlayOptions['options'])
            TexDefaultOptions.merge(options['frameOptions'], generalPairOptions)
            options['frameOptions'] = generalPairOptions
            generalPairOptions = dict(overlayOptions['options'])
            TexDefaultOptions.merge(options['connectorOptions'], generalPairOptions)
            options['connectorOptions'] = generalPairOptions
            def findNodeName(query, nodeDict):
                if type(query) == int:
                    res = [x for x in nodeDict.iteritems() if x[1]['index'] == query]
                elif type(query) == str:
                    res = [x for x in nodeDict.iteritems() if x[0] == query]
                else:
                    raise Exception("I don't understand the type!")
                if len(res) == 0:
                    raise Exception("I did not find the key %s!" % str(input))
                return res[0][1]['nodeName']
            options['nodeFrom'] = findNodeName(pair[0], completeScopeImages)
            options['nodeTo']   = findNodeName(pair[1], fieldOfViewImages)
            options['indicatorName'] = overlayOptions['indicatorNameBase'] + str(idx)
            options['frameName'] = overlayOptions['frameNameBase'] + str(idx)
            # calculate relative position in image!
            # calculate bend!

            
    @staticmethod
    def addGlobalOptionsToLocal(globalDict, localDict):
        options = ['indent', 'indentStep']
        for option in options:
            localDict[option] = globalDict[option]


                
                
        
        


if __name__ == "__main__":
    texDefaultOptions = TexDefaultOptions()
    someDict = {1 : 'b', 'a' : {'a' : 2}}
    print OptionParser.parse(texDefaultOptions.mergeUserOptions(someDict))




        

