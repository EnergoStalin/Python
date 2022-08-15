import os, requests, webbrowser, re, datetime, json, sys, time
import http.server
import socketserver

REQUEST_DATA = None
class RequestCapture(http.server.SimpleHTTPRequestHandler):
	def handle(self):
		global REQUEST_DATA

		data = self.rfile.read(1024)
		REQUEST_DATA = data.decode("utf-8")
		self.wfile.write(data)

def getToken(client_id, client_secret, scopes: list[str] = ["public"]):
	TOKEN = None
	if TOKEN: yield TOKEN

	if os.path.exists("creds.json"):
		with open("creds.json") as f:
			data = json.load(f)
			if(datetime.datetime.fromtimestamp(data["timestamp"]) + datetime.timedelta(seconds=data["expires_in"]) > datetime.datetime.now()):
				TOKEN = data["access_token"]
				yield TOKEN

	code = None
	with socketserver.TCPServer(("", 80), RequestCapture) as httpd:
		webbrowser.open_new_tab(f"https://osu.ppy.sh/oauth/authorize?client_id={client_id}&client_secret={client_secret}&response_type=code&scope={' '.join(scopes)}&redirect_uri={requests.utils.quote('http://localhost')}")
		httpd.handle_request()
		match = re.search(r"code=(.+?)\s", REQUEST_DATA)
		if(match): code = match[1]

	if(code):
		data = requests.post("https://osu.ppy.sh/oauth/token", {
			"client_id": client_id,
			"client_secret": client_secret,
			"code": code,
			"scope": " ".join(scopes),
			"grant_type": "client_credentials",
			"redirect_uri": "http://localhost"
		}).json()
		data["timestamp"] = datetime.datetime.now().timestamp()
		with open("creds.json", "w", encoding="utf-8") as f: json.dump(data, f)
		TOKEN = data["access_token"]

	yield TOKEN

def getBeatmapsetInfo(id):
	TOKEN = next(getToken('9088', ''))
	if TOKEN:
		return requests.get("https://osu.ppy.sh/api/v2/beatmapsets/" + str(id), headers={"Authorization": f"Bearer {TOKEN}"}).json()

def parseOsu(fp):
    data = None
    if os.path.exists(fp):
        with open(fp, encoding="utf-8") as f:
            data = f.read().split("\n")
    elif isinstance(fp, list):
        data = fp
    else:
        data = fp.split("\n")
    
    sections = {}
    cur_section = None
    for ln in data:
        if not(len(ln)):
            continue
        elif ln.startswith("["):
            cur_section = ln[1::][:-1]
            sections[cur_section] = {}
        elif cur_section in ["Events", "TimingPoints" , "HitObjects"]:
            continue
        elif cur_section:
            sections[cur_section].update([tuple(map(str.strip,ln.split(":", 1)))])
    return sections

def webUpdate(dr, upd):
	try:
		data = getBeatmapsetInfo(upd['Metadata'].get('BeatmapSetID', os.path.basename(dr).split(" ")[0]))
		upd["Metadata"]["Artist"] = data["artist"]
		upd["Metadata"]["Title"] = data["title"]
		return True
	except Exception as ex:
		print("Web update failed...", ex)

def main(root, forceWebUpdate = False):
	for p,_,f in os.walk(root): #Iter folders
		replacement = []
		for fn in f: #Iter files
			if fn.endswith(".osu"):
				with open(os.path.join(p,fn), "r+", encoding="utf-8") as fp:
					data = fp.read()
					osu = parseOsu(data)

					if forceWebUpdate: webUpdate(p,osu)

                    #Generating new filename
					ofn = osu["General"]["AudioFilename"]
					if not os.path.exists(os.path.join(p, ofn)):
						mp3s = list(filter(lambda x: x.endswith(".mp3"),next(os.walk(p))[2]))
						if(not len(mp3s)):
							print("Mp3 not found", p)
							continue
						ofn = os.path.basename(mp3s[0])

					nfn = None
					if len(replacement) and ofn == replacement[0]:
						nfn = replacement[1]
					else:
						if (osu['Metadata']['Artist'] and osu['Metadata']['Title']) or webUpdate(p, osu):
							nfn = f"{osu['Metadata']['Artist']} - {osu['Metadata']['Title']}{os.path.splitext(ofn)[1]}"
						else:
							print("No required data", os.path.join(p, fn))
							continue
					
					#Replacing data
					data = data.replace(ofn, nfn)
					
					#Renaming file if exists
					ofp = os.path.join(p,ofn)
					nfp = os.path.join(p,nfn)
					if os.path.exists(ofp) and not os.path.exists(nfp):
						os.rename(ofp, nfp)
						print(ofp, " -> ", nfp)
					else:
						print("Allready exists:", ofp, nfp)
					
					#Overwriting file
					fp.seek(0,0)
					fp.truncate(0)
					fp.write(data)
					
					#Store replacement
					replacement = [ofn, nfn]

if __name__ == "__main__":
	if(len(sys.argv) < 3):
		print("NEA")
	else:
		main(sys.argv[1], bool(sys.argv[2]))
