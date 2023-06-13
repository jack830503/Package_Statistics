##Enviorment:
macOS Catalina
Python 3.8.5

##Tools:
requests 2.24.0
bs4 4.12.2

##File Information:
debenv/: virtual enviornment
package_statistics.py: DebPackage class and main program
test_package_statistics.py: Unit test
output.png, output.txt: Show the result
test_output.png, test_output.txt: Show the result of test
README.md: Project Information 

##Install dependencies:
#Install the python virtual enviornment
python -m venv debenv
source debenv/bin/activate
pip3 install -r requirements.txt

##Process:
1. Send HTTP requests and fetch the response (HTML file).

2. Analyze the HTML file, build the "ContextList" dictionary that key is architecture; value is the compressed files which started with "Contents-" and associated with that architecture.

3. Search if argument is in "ContextList" and download the corresponding compressed file.

4. Parse each line in the file. Build the "PacList" dictionary to store package_name and counts of files associated with it.

5. Sort by counts of files associated with package in "PacList".

6. Output the statistics of top 10 packages_name.

##Run:
#main program
$ ./package_statistics.py $architecture

#test
$ python test_package_statistics.py

##Result:
I take "amd64" for example.  Excution time is 13 seconds containing download files.
I also run the test with unittest module in python. The Excution time for running 6 tests takes 86.769 seconds.


