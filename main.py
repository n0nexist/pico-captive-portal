# github.com/n0nexist/pico-captive-portal
from phew import logging, server, access_point, dns
from phew.template import render_template
from phew.server import redirect

# Configuration
DOMAIN = "wifi.login"
HTML_FILE = "index.html"
SSID = "Free Pico WiFi"

# Read the index.html file
@server.route("/", methods=['GET'])
def index(request):
    if request.method == 'GET':
        logging.debug("Got a hit on index.html")
        return render_template("index.html")

# WINDOWS
@server.route("/ncsi.txt", methods=["GET"])
def hotspot_windows(request):
    
    logging.info(f"Windows /ncsi.txt:\n{request}")
    return "", 200

# WINDOWS
@server.route("/connecttest.txt", methods=["GET"])
def hotspot_windows_connect_test(request):

    logging.info(f"Windows /connecttest.txt:\n{request}")
    return "", 200

# WINDOWS
@server.route("/redirect", methods=["GET"])
def hotspot_windows_redirect(request):
    
    logging.info(f"Windows /redirect:\n{request}")
    return redirect(f"http://{DOMAIN}/", 302)

# ANDROID
@server.route("/generate_204", methods=["GET"])
def hotspot_android(request):

    logging.info(f"Android /generate_204:\n{request}")
    return redirect(f"http://{DOMAIN}/", 302)

# APPLE
@server.route("/hotspot-detect.html", methods=["GET"])
def hotspot_apple(request):

    logging.info(f"Apple /hotspot-detect.html:\n{request}")
    return render_template("index.html")

# Other devices
@server.catchall()
def catch_all(request):

    logging.info(f"Caught dns request:\n{request}")
    return redirect("http://" + DOMAIN + "/")

# Main function
def main():
    ap = access_point(SSID)
    ip = ap.ifconfig()[0]
    logging.info(f"Pico's ip: \"{ip}\"")
    dns.run_catchall(ip)
    logging.info("Dns server started")
    server.run()
    logging.info("Web server started")

main()