import parse

def optParse(pattern, string,depth=0):
	#print("    "*depth + "Pattern: "+pattern)
	#print("    "*depth + "String:  "+string)
	#check for optional arguments (in brackets)
	res=(parse.parse("[{in}]{post}",pattern) or parse.parse("[{in}]",pattern) or parse.parse("{pre}[{in}]{post}",pattern) or parse.parse("{pre}[{in}]",pattern) or parse.parse("{pre}",pattern))

	#print("    "*depth + "Res:     " + str(res))

	if not res:
		#print("    "*depth + "Return:  None");
		return None

	inStr=""
	preStr=""
	postStr=""
	if("pre" in res.named):
		preStr=res["pre"]
	if("post" in res.named):
		postStr=res["post"]
	if("in" in res.named):
		inStr=res["in"]
		return optParse(preStr+inStr+postStr,string,depth+1) or optParse(preStr+postStr,string,depth+1)
	else:
		#print("    "*depth + "Return:  "+str(parse.parse(preStr,string)))
		return parse.parse(preStr,string)
