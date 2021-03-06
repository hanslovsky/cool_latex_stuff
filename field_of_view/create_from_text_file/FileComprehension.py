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
        'layers' : 'background,lower,middle,upper,main'
    },
    'completeScope' : {
        'layer' : 'lower',
        'meta' : {
            1 : { 
                'imageResolution' : (1600, 1097)
            }
        },
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
            },
            'example_images/arnie3.jpg' : {
                'index' : 3, 'options' : {}
            }
        },
        'nodeNameBase' : 'completeView',
        'options' : {},
    },
    'fieldOfViewScope' : {
        'options' : {},
        'scope' : {
            'options' : {
                'opacity' : 1.0,
                'yshift' : '-5cm'
            }
        },
        'lines' : {
            1 : {
                'options' : {},
                'scopeOptions' : {},
                'layer' : 'upper',
                'scale' : 'True',
                'images' : {
                    'example_images/arnie_vein1.jpg' : {
                        'index' : 1, 'options' : {}
                    },
                    'example_images/arnie_vein2.jpg' : {
                        'index' : 2, 'options' : {}
                    },
                    'example_images/arnie_vein3.jpg' : {
                        'index' : 3, 'options' : {}
                    },
                    'example_images/arnie_vein4.jpg' : {
                        'index' : 4, 'options' : {}
                    }
                    ,
                    'example_images/arnie_vein5.jpg' : {
                        'index' : 5, 'options' : {}
                    }
                    ,
                    'example_images/arnie_vein6.jpg' : {
                        'index' : 6, 'options' : {}
                    }
                    ,
                    'example_images/arnie_vein7.jpg' : {
                        'index' : 7, 'options' : {}
                    }
                    ,
                    'example_images/arnie_vein8.jpg' : {
                        'index' : 8
                        , 'options' : {}
                    }
                }
            },
        2 : {
                'options' : {},
                'scopeOptions' : {'yshift' : '-17cm'},
                'layer' : 'upper',
                'scale' : True,
                'images' : {
                    'example_images/arnie_ex1.jpg' : {
                        'index' : 1+8, 'options' : {'anchor' : 'north west'}
                    },
                    'example_images/arnie_ex2.jpg' : {
                        'index' : 2+8, 'options' : {}
                    },
                    'example_images/arnie_ex3.jpg' : {
                        'index' : 3+8, 'options' : {}
                    },
                    'example_images/arnie_ex4.jpg' : {
                        'index' : 4+8, 'options' : {}
                    },
                    'example_images/arnie_ex6.jpg' : {
                        'index' : 6+8, 'options' : {}
                    }
                }
            }
        },
        'fakeNameBase' : 'fake',
        'nodeNameBase' : 'fieldOfView',
    },
    'overlay' : {
        'frameLayer' : 'upper',
        'indicatorLayer' : 'upper',
        'connectorLayer' : 'middle',
        'scope' : {
            'options' : {
                'overlay' : None,
                'opacity' : 0.4
            }
        },
        'options' : {},
        'connectorOptions' : {
            'options' : {
                'fill' : 'red!30',
                'color' : 'black!70',
                'inner sep' : 0,
                'draw' : None,
                'thin' : None
            }
        },
        'frameOptions' : {
            'color' : 'red!70',
            'inner sep' : 0,
            'draw' : None,
            'ultra thick' : None
        },
        'indicatorOptions' : {
            'fill' : 'red!0',
            'color' : 'red!70',
            'inner sep' : 0,
            'draw' : None,
            'ultra thick' : None
        },
        'pairs' : {
            (1,2,1) : { 'frameOptions' : {'color' : 'blue!70'}, 'connectorOptions' : {'bend' : 0, 'options' : {'fill' : 'blue!30', 'color' : 'black!70'}}, 'indicatorOptions' : {}, 'type' : 1},
            (2,3,2) : { 'frameOptions' : {'color' : 'green!70'}, 'connectorOptions' : {'bend' : 5, 'options' : {'fill' : 'green!30', 'color' : 'black!70'}}, 'indicatorOptions' : {}, 'type' : 1},
            (3,8,3) : { 'frameOptions' : {}, 'connectorOptions' : {'bend' : 0, 'options' : {}}, 'indicatorOptions' : {}, 'type' : 1},
            (3,12,4) : { 'frameOptions' : {'color' : 'yellow!70'}, 'connectorOptions' : {'bend' : 0, 'options' : {'fill' : 'yellow!30', 'color' : 'black!70'}}, 'indicatorOptions' : {}, 'type' : 2},
            (1,9,5) : { 'frameOptions' : {'color' : 'orange!70'}, 'connectorOptions' : {'bend' : 0, 'options' : {'fill' : 'orange!30', 'color' : 'black!70'}}, 'indicatorOptions' : {}, 'type' : 2},
            (2,11,6) : { 'frameOptions' : {'color' : 'magenta!70'}, 'connectorOptions' : {'bend' : 0, 'options' : {'fill' : 'magenta!30', 'color' : 'black!70'}}, 'indicatorOptions' : {}, 'type' : 2}
        },
        'bend' : 0,
        'indicatorNameBase' : 'indicator',
        'frameNameBase' : 'frame',
        'meta' : {
            1 : {
                'originalKey' : 1,
                'indicatorResolution' : (200, 200),
                'indicatorPosition' : (70+200, 827)
            },
            2 : {
                'originalKey' : 1,
                'indicatorResolution' : (200, 200),
                'indicatorPosition' : (70, 1027)
            }
        }
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
        OptionParser.parseOverlayOptions(overlayOptions, completeScopeOptions, fieldOfViewScopeOptions)

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
                fakeOptions = copy.deepcopy(options)
                fakeOptions['nodeName'] = fieldOfViewScopeOptions['fakeNameBase'] + str(options['index'])
                if prevKey > -1:
                    options['options']['right'] = 'of %s%d' % (fieldOfViewScopeOptions['nodeNameBase'], prevKey)
                    fakeOptions['options']['right'] = 'of %s%d' % (fieldOfViewScopeOptions['fakeNameBase'], prevKey)
                fakeKeyValuePairs.append((image, fakeOptions, line))
                keyValuePairs.append((image, options, line))
                prevKey = int(options['index'])
        fieldOfViewScopeOptions['images'] = {}
        fieldOfViewScopeOptions['fakes']  = {}
        for key, value, line in keyValuePairs:
            if not 'images' in fieldOfViewScopeOptions['lines'][line].keys():
                fieldOfViewScopeOptions['lines'][line]['images'] = {}
            fieldOfViewScopeOptions['lines'][line]['images'][key] = value
            fieldOfViewScopeOptions['images'][key] = value
        for key, value, line in fakeKeyValuePairs:
            if not 'fakes' in fieldOfViewScopeOptions['lines'][line].keys():
                fieldOfViewScopeOptions['lines'][line]['fakes'] = {}
            fieldOfViewScopeOptions['lines'][line]['fakes'][key] = value
            fieldOfViewScopeOptions['fakes'][key] = value


    @staticmethod
    def parseOverlayOptions(overlayOptions, completeScopeOptions, fieldOfViewOptions):
        completeScopeImages = completeScopeOptions['images']
        fieldOfViewImages   = fieldOfViewOptions['images']
        pairs = overlayOptions['pairs']
        nPairs = len(pairs.keys())
        start = overlayOptions['bend']
        if int(start) == 0:
            bendValues = [0]*nPairs
        else:
            step = 2.0*start/float(nPairs-1)
            def frange(start, stop, step):
                while start < stop:
                    yield start
                    start += step
            bendValues = [int(x) for x in frange(-start, start+step, step)]
        assert str(len(bendValues)) + " bend values, but " + str(nPairs) + "  pairs" and len(bendValues) == nPairs
        
        generalPairOptions = dict(overlayOptions['options'])
        TexDefaultOptions.merge(overlayOptions['frameOptions'], generalPairOptions)
        overlayOptions['frameOptions'] = generalPairOptions
        generalPairOptions = dict(overlayOptions['options'])
        TexDefaultOptions.merge(overlayOptions['connectorOptions']['options'], generalPairOptions)
        overlayOptions['connectorOptions']['options'] = generalPairOptions
        generalPairOptions = dict(overlayOptions['options'])
        TexDefaultOptions.merge(overlayOptions['indicatorOptions'], generalPairOptions)
        overlayOptions['indicatorOptions'] = generalPairOptions
            
        for idx, (pair, options) in enumerate(sorted(pairs.iteritems(),key=lambda x: int(x[0][0]))):
            generalPairOptions = dict(overlayOptions['frameOptions'])
            TexDefaultOptions.merge(options['frameOptions'], generalPairOptions)
            options['frameOptions'] = generalPairOptions
            generalPairOptions = copy.deepcopy(overlayOptions['connectorOptions'])
            TexDefaultOptions.merge(options['connectorOptions'], generalPairOptions)
            options['connectorOptions'] = generalPairOptions
            generalPairOptions = dict(overlayOptions['options'])
            TexDefaultOptions.merge(options['indicatorOptions'], generalPairOptions)
            options['indicatorOptions'] = generalPairOptions
            def findNodeName(query, nodeDict):
                if type(query) == int:
                    res = [x for x in nodeDict.iteritems() if x[1]['index'] == query]
                elif type(query) == str:
                    raise Exception, "Does not support string as index for nodes"
                    res = [x for x in nodeDict.iteritems() if x[0] == query]
                else:
                    raise Exception("I don't understand the type!")
                if len(res) == 0:
                    raise Exception("I did not find the key %s!" % str(input))
                return res[0][1]['nodeName']
            options['nodeFrom'] = findNodeName(pair[0], completeScopeImages)
            options['nodeTo']   = findNodeName(pair[1], fieldOfViewImages)
            options['indicatorName'] = overlayOptions['indicatorNameBase'] + str(idx)
            typeId = options['type']
            originalKey = overlayOptions['meta'][typeId]['originalKey']
            position = list(overlayOptions['meta'][typeId]['indicatorPosition'])
            resolution = list(overlayOptions['meta'][typeId]['indicatorResolution'])
            # take care of inverted y axis for tikz
            position[1]   = completeScopeOptions['meta'][originalKey]['imageResolution'][1] - position[1]
            options['relativeIndicatorPosition'] = \
              (float(position[0])/completeScopeOptions['meta'][originalKey]['imageResolution'][0],
               float(position[1])/completeScopeOptions['meta'][originalKey]['imageResolution'][1])
            # overlayOptions['meta'][typeId]['relativeIndicatorPosition'] = \
            #   (float(position[0])/completeScopeOptions['meta'][originalKey]['imageResolution'][0],
            #    float(position[1])/completeScopeOptions['meta'][originalKey]['imageResolution'][1])
            options['relativeIndicatorResolution'] = \
              (float(resolution[0])/completeScopeOptions['meta'][originalKey]['imageResolution'][0],
               float(resolution[1])/completeScopeOptions['meta'][originalKey]['imageResolution'][1])
            # overlayOptions['meta'][typeId]['relativeIndicatorResolution'] = \
            #   (float(overlayOptions['indicatorResolution'][0])/completeScopeOptions['imageResolution'][0],
            #    float(overlayOptions['indicatorResolution'][1])/completeScopeOptions['imageResolution'][1])
                                                              
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




        

