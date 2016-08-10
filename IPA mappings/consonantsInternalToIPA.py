
consonantsInternalToIPA = {
#hundreds digit refers to row, 10s digit to labial/coronal/dorsal/laryngeal, ones to subcolumn (ones are 1 indexed, rest are 0), 
#half refers to the voiced variant where voiced and voiceless both exist
	# 1.0: 'm_0', #bilabial nasal voiceless #unicode not available? 
	1.5: u'\u006D', #bilabial nasal voiced 
	2.0: u'\u0271', #labiodental nasal
	3.0: u'\u006E\u033C', #linguolabial nasal 
	12.0: 'n_0', #voiceless alveolar nasal
	12.5: u'\u006E', #voiced alveolar nasal 
	14.0: u'\u0273', #retroflex nasal
	22.0: u'\u0272', #palatal nasal
	23.0: u'\u014B', #velar nasal
	23.25: u'\u014B\u0361\u006D', #labial-velar nasal COART
	24.0: u'\u0274', #uvular nasal
	101.0: u'\u0070', #voiceless bilabial stop
	101.5: u'\u0062', #voiced bilabial stop
	102.0: u'\u0070\u032A', #voiceless labiodental stop
	102.5: u'\u0062\u032A', #voiced labiodental stop
	113.0: u'\u0074', #voiceless alveolar stop
	113.5: u'\u0064', #voiced alveolar stop
	114.0: u'\u0288', #voiceless retroflex stop
	114.5: u'\u0256', #voiced retroflex stop
	122.0: u'\u0063', #voiceless palatal stop
	122.5: u'\u025F', #voiced palatal stop
	123.0: u'\u006B', #voiceless velar stop
	123.25: u'\u006B\u0361\u0070', #voiceless labial-velar stop COART
	123.5: u'\u0261', #voied velar stop
	123.75: u'\u0261\u0361\u0062', #voiced labial-velar stop COART
	124.0: u'\u0071', #voiceless uvular stop
	124.5: u'\u0262', #voiced uvular stop
	131.0: u'\u02A1', #epiglottal stop
	132.0: u'\u0294', #glottal stop
	212.0: u'\u02A6', #voiceless alveolar sibilant affricate
	212.5: u'\u02A3', #voiced alveolar sibilant affricate
	214.0: u'\u0074\u0361\u0283', #voiceless palato-alveolar sibilant affricate
	214.5: u'\u0064\u0361\u0292', #voiced palato-alveolar sibilant affricate
	214.0: u'\u0288\u0361\u0282', #voiceless retroflex sibilant affricate
	214.5: u'\u0256\u0361\u0290', #voiced retroflex sibilant affricate
	221.0: u'\u02A8', #voiceless alveolo-palatal sibilant affricate
	221.5: u'\u02A5', #voiced alveolo-palatal sibilant affricate
	322.0: u'\u0063\u0361\u00E7', #voiceless palatal affricate
	322.5: u'\u025F\u0361\u029D', #voiced palatal affricate
	422.0: u'\u0073', #voiceless alveolar sibilant
	422.5: u'\u007A', #voiced alveolar sibilant
	423.0: u'\u0283', #voiceless palato-alveolar sibilant
	423.5: u'\u0292', #voiced palato-alveolar sibilant
	424.0: u'\u0282', #voiceless retroflex sibilant
	424.5: u'\u0290', #voiced retroflex sibilant
	431.0: u'\u0255', #voiceless alveolo-palatal sibilant
	432.5: u'\u0291', #voiced alveolo-palatal sibilant 
	501.0: u'\u0278', #voiceless bilabial fricative
	501.5: u'\u03B2', #voiced bilabial fricative
	502.0: u'\u0066', #voicless labiodental fricative
	502.5: u'\u0076', #voiced labiodental fricative
	511.0: u'\u03B8', #voiceless dental fricative
	511.5: u'\u00F0', #voiced dental fricative
	512.0: u'\u03B8\u0331', #voiceless alveolar non-sibilant fricative
	512.5: u'\u00F0\u0320', #voiced alveolar non-sibilant fricative
	522.0: u'\u00E7', #voiceless palatal fricative
	522.5: u'\u029D', #voiced palatal fricative
	523.0: u'\u0078', #voiceless velar fricative
	523.25: u'\u0267', #voiceless palatal-velar fricative COART
	523.5: u'\u0263', #voiced velar fricative
	524.0: u'\u03C7', #voiceless uvular fricative
	524.5: u'\u0281', #voiced uvular fricative
	531.0: u'\u0127', #voiceless pharyngeal fricative
	531.5: u'\u0295', #voiced pharyngeal fricative
	532.0: u'\u0068', #voiceless glottal fricative
	532.5: u'\u0266', #voiced glottal fricative
	602.0: u'\u028B', #labiodental approximant
	622.0: u'\u0279', #alveolar approximant
	624.0: u'\u027B', #retroflex approximant
	632.0: u'\u006A\u030A', #voiceless palatal approximant
	632.25: u'\u0265', #labialized palatal approximant COART
	632.5: u'\u006A', #voiced palatal approximant
	633.0: u'\u028D', #voiceless labialized velar approximant COART
	633.25: u'\u0077', #voiced labio-velar approximant COART
	633.5: u'\u0270', #voiced velar approximant 
	701.0: u'\u2C71\u031F', #bilabial flap
	702.0: u'\u2C71', #labiodental flap
	712.0: u'\u027E', #alveolar flap
	714.0: u'\u027D', #retroflex flap
	724.5: u'\u0262\u0306', #uvular flap
	801.5: u'\u0299', #bilabial trill
	812.0: 'r_0', 	#voiceless alveolar trill
	812.5: u'\u0072', #voiced alveolar trill
	814.5: u'\u027D\u0361\u0072', #voiced retroflex trill
	824.5: u'\u0280', #uvular trill
	831.0: u'\u029C', #voiceless epiglottal trill
	831.5: u'\u02A2', #voiced epiglottal trill
	912.0: u'\u0074\u0361\u026C', #voiceless alveolar lateral affricate
	912.5: u'\u0064\u0361\u026E', #voiced alveolar lateral affricate
	1012.0: u'\u026C', #voiceless alveolar lateral fricative
	1012.5: u'\u026E', #voiced alveolar lateral fricative
	1022.0: u'\u028E\u0325\u02D4', #voiceless palatal lateral fricative
	1112.5: u'\u006C', #alveolar lateral approximant
	1114.5: u'\u026D', #retroflex lateral approximant
	1122.0: u'\u028E', #palatal lateral approximant
	1123.5: u'\u029F', #voiced velar lateral approximant
	1212.5: u'\u027A', #alveolar lateral flap



##TODO: Add non-pulmonic consonants	



}
