from openalpr import Alpr
import sys

alpr = Alpr("us", "/home/dhruv/openalpr/src/build/config/openalpr.conf", "/home/dhruv/openalpr/runtime_data/")
if not alpr.is_loaded():
    print("Error loading OpenALPR")
    sys.exit(1)
    
alpr.set_top_n(20)
alpr.set_default_region("go")

results = alpr.recognize_file("/home/dhruv/openalpr/src/build/f.jpg")
print(results)
i = 0
for plate in results['results']:
    i += 1
    print("Plate #%d" % i)
    print("   %12s %12s" % ("Plate", "Confidence"))
    for candidate in plate['candidates']:
        prefix = "-"
        if candidate['matches_template']:
            prefix = "*"

        print("  %s %12s%12f" % (prefix, candidate['plate'], candidate['confidence']))

# Call when completely done to release memory
alpr.unload()