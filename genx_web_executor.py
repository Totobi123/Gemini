
import http.server, socketserver, json, webbrowser, threading, smtplib, ssl, time, random, os, socket, concurrent.futures, sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr

# --- LOCK FOR HISTORY ---
HISTORY_LOCK = threading.Lock()

# --- EMBEDDED DATA ---
TARGETS = [
    {
        "ceo_name": "Jere Morehead",
        "employee_name": "Bryce Mclester",
        "email": "bryce.mclester@uga.edu"
    },
    {
        "ceo_name": "Pujun Bhatnagar",
        "employee_name": "Gautam Gupta",
        "email": "gautam@trykintsugi.com"
    },
    {
        "ceo_name": "Neeli Bendapudi",
        "employee_name": "Akil Creswell",
        "email": "akil-creswell@psu.edu"
    },
    {
        "ceo_name": "Maurie McInnis",
        "employee_name": "Julia Peet",
        "email": "julia.peet@yale.edu"
    },
    {
        "ceo_name": "Michael Hellman",
        "employee_name": "Swayam Arora",
        "email": "swayam.arora@acmutd.co"
    },
    {
        "ceo_name": "Donald W. Landry",
        "employee_name": "Sarthak Gupta",
        "email": "sarthak.gupta@ufl.edu"
    },
    {
        "ceo_name": "Molysa Hang",
        "employee_name": "Mikhail Maredia",
        "email": "maredia_mikhail@uhabsa.org"
    },
    {
        "ceo_name": "Ángel Cabrera",
        "employee_name": "Anson G",
        "email": "anson.g@gatech.edu"
    },
    {
        "ceo_name": "Jaia Thomas",
        "employee_name": "Sanai Anderson",
        "email": "sanai@diverserepresentation.com"
    },
    {
        "ceo_name": "Michael Khan",
        "employee_name": "Rishita Mishra",
        "email": "rishita.mishra@smu.ca"
    },
    {
        "ceo_name": "Donald W. Landry",
        "employee_name": "Laura María Garzón",
        "email": "laura@ufl.edu"
    },
    {
        "ceo_name": "Chantilly, Virginia",
        "employee_name": "Vincent N",
        "email": "vincent.n@aimic.com"
    },
    {
        "ceo_name": "Michael Bego",
        "employee_name": "Phillip Babuscio",
        "email": "phillip.babuscio@klinehill.com"
    },
    {
        "ceo_name": "Yijun Huang",
        "employee_name": "Janet Holland",
        "email": "jholland@meritcro.com"
    },
    {
        "ceo_name": "Richard McCullough",
        "employee_name": "Upamanyu Shanker",
        "email": "ushanker@fsu.edu"
    },
    {
        "ceo_name": "Darryll Pines",
        "employee_name": "Ojas Jagtap",
        "email": "ojagtap@umd.edu"
    },
    {
        "ceo_name": "Naomi Rodriguez",
        "employee_name": "Rafael J",
        "email": "rafael@eralifecare.com"
    },
    {
        "ceo_name": "HK Lee",
        "employee_name": "Bryan Sandora",
        "email": "bryans@digital-watchdog.com"
    },
    {
        "ceo_name": "Ronald L. Ellis",
        "employee_name": "Benjamin Solomon",
        "email": "bsolomon@calbaptist.edu"
    },
    {
        "ceo_name": "Radenka Maric",
        "employee_name": "Evan Franco",
        "email": "evan.franco@uconn.edu"
    },
    {
        "ceo_name": "John Carroll",
        "employee_name": "Connor Stahl",
        "email": "cstahl@svdisposition.com"
    },
    {
        "ceo_name": "Marty Meehan",
        "employee_name": "Saketh Jeedigunta",
        "email": "sjeedigunta@umass.edu"
    },
    {
        "ceo_name": "Stacy Milner",
        "employee_name": "Tereik Faulknor",
        "email": "tereik@eicop.org"
    },
    {
        "ceo_name": "Dilpreet Sahota",
        "employee_name": "Karan Birdi",
        "email": "karan@trekhealth.io"
    },
    {
        "ceo_name": "Michael J. Cavanagh",
        "employee_name": "Lawrence Durudogan",
        "email": "lawrence.durudogan@nbcuni.com"
    },
    {
        "ceo_name": "Ron Zayas",
        "employee_name": "Shon Smillie",
        "email": "shon@ironwall.com"
    },
    {
        "ceo_name": "Brent Shedd",
        "employee_name": "Brandon Liu",
        "email": "brandon@agrobotics.com"
    },
    {
        "ceo_name": "Donald W. Landry",
        "employee_name": "Mary Slowik",
        "email": "maryslowik@ufl.edu"
    },
    {
        "ceo_name": "Guillermo Rauch",
        "employee_name": "Melody Chang",
        "email": "melody.chang@vercel.com"
    },
    {
        "ceo_name": "Jennifer Mnookin",
        "employee_name": "Ramon Guarnero",
        "email": "guarnero@wisc.edu"
    },
    {
        "ceo_name": "Alex Gunnarson",
        "employee_name": "Anish Krishnan",
        "email": "anish@onton.com"
    },
    {
        "ceo_name": "Brady See",
        "employee_name": "Thandeka Mudavanhu",
        "email": "tmudavanhu@illinoisbusinesscouncil.com"
    },
    {
        "ceo_name": "Terry Kerr",
        "employee_name": "Trey Lamanna",
        "email": "trey@midsouthhomebuyers.com"
    },
    {
        "ceo_name": "Brent Gendleman",
        "employee_name": "Melissa Pham",
        "email": "mpham@agilian.com"
    },
    {
        "ceo_name": "Saara Hassoun",
        "employee_name": "Chelsea Knutson",
        "email": "chelsea@mnaurora.com"
    },
    {
        "ceo_name": "Corinne Pierog",
        "employee_name": "Daniel Omalley",
        "email": "omalleydaniel@countyofkane.org"
    },
    {
        "ceo_name": "Laird Rixford",
        "employee_name": "Alvaro Angel",
        "email": "aangel@instechnologies.net"
    },
    {
        "ceo_name": "Kent Syverud",
        "employee_name": "Dream Patel",
        "email": "dpatel@syracuse.edu"
    },
    {
        "ceo_name": "Joan Gabel",
        "employee_name": "Nischal Kharel",
        "email": "nkharel@pitt.edu"
    },
    {
        "ceo_name": "Kiron Chandy",
        "employee_name": "Shyla Bhandari",
        "email": "shyla.bhandari@consultyourcommunity.org"
    },
    {
        "ceo_name": "Donald P. Lloyd",
        "employee_name": "Mason Braithwaite",
        "email": "mason.braithwaite@afstores.com"
    },
    {
        "ceo_name": "Edward J. Feser",
        "employee_name": "Casey Masterson",
        "email": "casey.masterson@slu.edu"
    },
    {
        "ceo_name": "Filip Aronshtein",
        "employee_name": "Nathan Varghese",
        "email": "nathan@diracinc.com"
    },
    {
        "ceo_name": "D. Game",
        "employee_name": "Raya Rowan",
        "email": "rrowan@geominex.com"
    },
    {
        "ceo_name": "Ajantha Ganeshalingam",
        "employee_name": "Rishane Jesuretnam",
        "email": "rishane@fintexinc.com"
    },
    {
        "ceo_name": "Tim Cook",
        "employee_name": "Aurea Mcintosh",
        "email": "aurea.mcintosh@us.apple.com"
    },
    {
        "ceo_name": "Ken Daley",
        "employee_name": "Ali Alsaymary",
        "email": "aalsaymary@indianatollroad.org"
    },
    {
        "ceo_name": "Neeli Bendapudi",
        "employee_name": "Olivia Bartholomew",
        "email": "olivia-bartholomew@psu.edu"
    },
    {
        "ceo_name": "Dennis Assanis",
        "employee_name": "Bahaar Ahuja",
        "email": "bahaarahuja@ucsb.edu"
    },
    {
        "ceo_name": "Lisa Freeman",
        "employee_name": "Chirag Singh",
        "email": "csingh@niu.edu"
    },
    {
        "ceo_name": "Douglas Girod",
        "employee_name": "Heagen Bell",
        "email": "heagenbell@ku.edu"
    },
    {
        "ceo_name": "Joan Gabel",
        "employee_name": "Simon Fisher",
        "email": "sfisher@pitt.edu"
    },
    {
        "ceo_name": "Richard Lyons",
        "employee_name": "Cooper Owen",
        "email": "cooper@berkeley.edu"
    },
    {
        "ceo_name": "Melanie Woodin",
        "employee_name": "Kayla Chow",
        "email": "k.chow@utoronto.ca"
    },
    {
        "ceo_name": "Farnam Jahanian",
        "employee_name": "Timothy Wright",
        "email": "wright@cmu.edu"
    },
    {
        "ceo_name": "Charlene Prosnik",
        "employee_name": "Anthony Youmans",
        "email": "ayoumans@capfixtures.com"
    },
    {
        "ceo_name": "Prabhas Moghe",
        "employee_name": "Sai Chauhan",
        "email": "sai.chauhan@utdallas.edu"
    },
    {
        "ceo_name": "W.H. Hamilton",
        "employee_name": "Jan Gabriel Dizon",
        "email": "jdizon@millards.com"
    },
    {
        "ceo_name": "Josephine Tjhia",
        "employee_name": "Jessica Ocampo",
        "email": "jessica@hackthevalley.io"
    },
    {
        "ceo_name": "Maurie McInnis",
        "employee_name": "Daysha Selena Williams",
        "email": "daysha.williams@yale.edu"
    },
    {
        "ceo_name": "Craig Behm",
        "employee_name": "Christal Forte",
        "email": "christal.forte@crisphealth.org"
    },
    {
        "ceo_name": "Christopher Wunder",
        "employee_name": "Vito Finetti",
        "email": "vito@leapbrands.io"
    },
    {
        "ceo_name": "Pamela Whitten",
        "employee_name": "Lakshmi Ajith",
        "email": "lajith@iu.edu"
    },
    {
        "ceo_name": "Timothy Sands",
        "employee_name": "Nicholas Restina",
        "email": "nicholas@vt.edu"
    },
    {
        "ceo_name": "Suresh Garimella",
        "employee_name": "Duo Bao",
        "email": "duo@arizona.edu"
    },
    {
        "ceo_name": "John Weber",
        "employee_name": "Ryan Royse",
        "email": "rroyse@softwaretoolbox.com"
    },
    {
        "ceo_name": "Gary May",
        "employee_name": "Kevin Bui",
        "email": "kbui@ucdavis.edu"
    },
    {
        "ceo_name": "Erik Prusch",
        "employee_name": "Rhiya Prasad",
        "email": "rprasad@isaca.org"
    },
    {
        "ceo_name": "Joseph E. Aoun",
        "employee_name": "Lisa Ju",
        "email": "lisa.j@northeastern.edu"
    },
    {
        "ceo_name": "Richard McCullough",
        "employee_name": "Ashley Zapata",
        "email": "azapata@fsu.edu"
    },
    {
        "ceo_name": "Jason Mickool",
        "employee_name": "Austin Shoopman",
        "email": "austin.shoopman@texasfa.com"
    },
    {
        "ceo_name": "Andrea Goldsmith",
        "employee_name": "Arin Mohanty",
        "email": "arin.mohanty@stonybrook.edu"
    },
    {
        "ceo_name": "Alan Frank",
        "employee_name": "Mia Brown",
        "email": "mia@chimneyrockinn.com"
    },
    {
        "ceo_name": "Mark Hunker",
        "employee_name": "Ethan Bunkley",
        "email": "ethan.bunkley@secured.team"
    },
    {
        "ceo_name": "Richard Lyons",
        "employee_name": "Tanya Sun",
        "email": "tanya@berkeley.edu"
    },
    {
        "ceo_name": "Laura-Kathryn Neal",
        "employee_name": "Pranita Mishra",
        "email": "pranita@achecf.org"
    },
    {
        "ceo_name": "Joe Kuntar",
        "employee_name": "Bennett Santus",
        "email": "bsantus@mgccgolf.us.com"
    },
    {
        "ceo_name": "Clark May",
        "employee_name": "Mandikar White",
        "email": "mwhite@opoc.us"
    },
    {
        "ceo_name": "Shabnam Naz Ansari",
        "employee_name": "Gursaajan Singh",
        "email": "gursaajan@volunteer-well.org"
    },
    {
        "ceo_name": "Michael I. Kotlikoff",
        "employee_name": "Bernebas Mehari",
        "email": "mehari@cornell.edu"
    },
    {
        "ceo_name": "Eli Capilouto",
        "employee_name": "Kailey Strausbaugh",
        "email": "kailey.strausbaugh@uky.edu"
    },
    {
        "ceo_name": "William Tate",
        "employee_name": "Shruthi Raju",
        "email": "shruthi.raju@rutgers.edu"
    },
    {
        "ceo_name": "Michael I. Kotlikoff",
        "employee_name": "Emiline Labbe",
        "email": "labbe@cornell.edu"
    },
    {
        "ceo_name": "Lisa Hillman",
        "employee_name": "Sardar Gul",
        "email": "sgul@exceptionalwellnesscounseling.com"
    },
    {
        "ceo_name": "Andrew Qian, Cynthia Lan",
        "employee_name": "Cynthia Lan",
        "email": "cynthia@cornelldti.org"
    },
    {
        "ceo_name": "Timothy Sands",
        "employee_name": "Rohan Praveen Chavan",
        "email": "rohan@vt.edu"
    },
    {
        "ceo_name": "Rajshekhar P",
        "employee_name": "Prethivi Vs",
        "email": "prethivi@isacfoundation.org"
    },
    {
        "ceo_name": "Tom Nelson",
        "employee_name": "Carlie Gregg",
        "email": "carlieg@cckc.church"
    },
    {
        "ceo_name": "Jason Maynard",
        "employee_name": "Curtis Greenwood",
        "email": "curtis-greenwood@qualtrics.com"
    },
    {
        "ceo_name": "Sven Wiedenhaupt",
        "employee_name": "Brendan Miller",
        "email": "bmiller@lakenonawavehotel.com"
    },
    {
        "ceo_name": "Peter J. Mohler",
        "employee_name": "Lauren Olivia Williams",
        "email": "lwilliams@ua.edu"
    },
    {
        "ceo_name": "Thomas Anderson",
        "employee_name": "Ankit Bhandari",
        "email": "abhandari@studentsunited.org"
    },
    {
        "ceo_name": "Keith Goldsmith",
        "employee_name": "Krati Jadaun",
        "email": "krati.jadaun@realcold.com"
    },
    {
        "ceo_name": "Richard McCullough",
        "employee_name": "Enchi Zheng",
        "email": "ezheng@fsu.edu"
    },
    {
        "ceo_name": "Thomas Patton",
        "employee_name": "Isabella Hughes",
        "email": "isabella.hughes@miamidsp.com"
    },
    {
        "ceo_name": "Richard Lyons",
        "employee_name": "Karen Tian",
        "email": "tiankaren@berkeley.edu"
    },
    {
        "ceo_name": "Peter J. Mohler",
        "employee_name": "Mallory Cook",
        "email": "mcook@ua.edu"
    },
    {
        "ceo_name": "Mahima Agrawal",
        "employee_name": "Amulya Monangi",
        "email": "amulya.monangi@nobeillinois.org"
    },
    {
        "ceo_name": "Marlene Tromp",
        "employee_name": "Jane Bregenzer",
        "email": "jane.bregenzer@uvm.edu"
    },
    {
        "ceo_name": "Jeffrey D. Armstrong",
        "employee_name": "Anagha Kulkarni",
        "email": "akulkarni@calpoly.edu"
    },
    {
        "ceo_name": "Isaac Martinez",
        "employee_name": "Vanessa Chok",
        "email": "vanessachok@ucidsp.com"
    },
    {
        "ceo_name": "Angela Cain",
        "employee_name": "Matthew Devin",
        "email": "matthew.devin@uli.org"
    },
    {
        "ceo_name": "Fasil KK",
        "employee_name": "Abdul Samad",
        "email": "samad@iocod.com"
    },
    {
        "ceo_name": "Jennifer des Groseilliers",
        "employee_name": "Sabrina Nafia",
        "email": "s.nafia@themathergroup.com"
    },
    {
        "ceo_name": "Kate Jarvis",
        "employee_name": "Ben Schaffer",
        "email": "ben@fifthdimensionai.com"
    },
    {
        "ceo_name": "Joseph E. Aoun",
        "employee_name": "Aryan Jain",
        "email": "jain.aryan@northeastern.edu"
    },
    {
        "ceo_name": "George Jacobs",
        "employee_name": "Majd Saleh",
        "email": "msaleh@windycitylimos.com"
    },
    {
        "ceo_name": "Donald W. Landry",
        "employee_name": "Carolina Alfonso",
        "email": "carolinaalfonso@ufl.edu"
    },
    {
        "ceo_name": "Justin Sparks",
        "employee_name": "Sophie Messinger",
        "email": "sophie.messinger@pivitglobal.com"
    },
    {
        "ceo_name": "Jere Morehead",
        "employee_name": "Audrey Djunaidi",
        "email": "audrey.djunaidi@uga.edu"
    },
    {
        "ceo_name": "Donald W. Landry",
        "employee_name": "Isabella Marin",
        "email": "isabellamarin@ufl.edu"
    },
    {
        "ceo_name": "Michael Mazur",
        "employee_name": "Tyler Price",
        "email": "t.price@aiclearing.com"
    },
    {
        "ceo_name": "Brady See",
        "employee_name": "Drew Bowen",
        "email": "dbowen@illinoisbusinesscouncil.com"
    },
    {
        "ceo_name": "James Davis",
        "employee_name": "Allen Huang",
        "email": "huang@utexas.edu"
    },
    {
        "ceo_name": "Brandon Raboin",
        "employee_name": "Jaiden Yaeger",
        "email": "jaiden@raboinrealty.com"
    },
    {
        "ceo_name": "Nancy Li",
        "employee_name": "Abhinav R",
        "email": "abhinav@pmaccelerator.io"
    },
    {
        "ceo_name": "Kyra van den Bosch",
        "employee_name": "Duncan Shaver",
        "email": "duncan.shaver@highwire.com"
    },
    {
        "ceo_name": "Howard Gillman",
        "employee_name": "Jerry Nguyen",
        "email": "jnguyen@uci.edu"
    },
    {
        "ceo_name": "Pamela Whitten",
        "employee_name": "Brinda Samula",
        "email": "bsamula@iu.edu"
    },
    {
        "ceo_name": "Julie Sullivan",
        "employee_name": "Aidan Auyeung",
        "email": "aauyeung@scu.edu"
    },
    {
        "ceo_name": "Tara Maddala",
        "employee_name": "York Li",
        "email": "york@pandorabio.com"
    },
    {
        "ceo_name": "James Penman",
        "employee_name": "Brody Rukenbrod",
        "email": "brukenbrod@donnellypenman.com"
    },
    {
        "ceo_name": "Kevin Guskiewicz",
        "employee_name": "Parker Isham",
        "email": "ishamp@msu.edu"
    },
    {
        "ceo_name": "Anthony Casalena",
        "employee_name": "Nicolas Parodi",
        "email": "nicolasparodi@squarespace.com"
    },
    {
        "ceo_name": "Gary May",
        "employee_name": "Anisha Vikash",
        "email": "avikash@ucdavis.edu"
    },
    {
        "ceo_name": "Srikanth Gundavarapu",
        "employee_name": "Nicolas Blakey",
        "email": "nicolas.blakey@sewausa.org"
    },
    {
        "ceo_name": "Andrew D. Martin",
        "employee_name": "Palladium Liang",
        "email": "liang@wustl.edu"
    },
    {
        "ceo_name": "James Davis",
        "employee_name": "David Nguyen",
        "email": "david@utexas.edu"
    },
    {
        "ceo_name": "Grant Martin",
        "employee_name": "Isaiah Ritenour",
        "email": "isaiah@mag.industries"
    },
    {
        "ceo_name": "Tony Thrush",
        "employee_name": "Claire Cosier",
        "email": "claire.cosier@iowastatedaily.com"
    },
    {
        "ceo_name": "Michael Amiridis",
        "employee_name": "Ava Billotto",
        "email": "avabillotto@sc.edu"
    },
    {
        "ceo_name": "Alan Garber",
        "employee_name": "Oksana Trefanenko",
        "email": "oksana_trefanenko@harvard.edu"
    },
    {
        "ceo_name": "Moez Limayem",
        "employee_name": "Maira Hanif",
        "email": "mhanif@usf.edu"
    },
    {
        "ceo_name": "Dennis Assanis",
        "employee_name": "Benjamin Oh",
        "email": "benjaminoh@ucsb.edu"
    },
    {
        "ceo_name": "Andrea Kemp-Curtis",
        "employee_name": "Suma Narra",
        "email": "suma.narra@potomac.edu"
    },
    {
        "ceo_name": "Iqbal Sheikh",
        "employee_name": "Axel Van Der Maal",
        "email": "axel.vandermaal@cybertex.edu"
    },
    {
        "ceo_name": "Jake Seaton",
        "employee_name": "Ryan Beeler",
        "email": "rbeeler@column.com"
    },
    {
        "ceo_name": "George Jones",
        "employee_name": "Kyle Gragnola",
        "email": "kyle@jonessportsco.com"
    },
    {
        "ceo_name": "Brian Shore",
        "employee_name": "Addison Foreman",
        "email": "aforeman@parkelectro.com"
    },
    {
        "ceo_name": "Donald W. Landry",
        "employee_name": "Sargam Thakur",
        "email": "thakur.s@ufl.edu"
    },
    {
        "ceo_name": "Randy Boyd",
        "employee_name": "Ciara Mcmahon",
        "email": "ciara@utk.edu"
    },
    {
        "ceo_name": "Joseph Harroz",
        "employee_name": "Marshall Tapfuma",
        "email": "mtapfuma@ou.edu"
    },
    {
        "ceo_name": "Michael I. Kotlikoff",
        "employee_name": "Justin Eburuoh",
        "email": "justine@cornell.edu"
    },
    {
        "ceo_name": "Loudin Cato",
        "employee_name": "Anika Kapil",
        "email": "akapil@ufdsp.com"
    },
    {
        "ceo_name": "Ralf Ledda",
        "employee_name": "Alexandra Mcpartland",
        "email": "alexandra.mcpartland@hettweb.com"
    },
    {
        "ceo_name": "Jack Schulz",
        "employee_name": "Srikanth Gopu",
        "email": "srikanth.gopu@clark-ind.com"
    },
    {
        "ceo_name": "Michael Crow",
        "employee_name": "Alay Patel",
        "email": "alay.patel@asu.edu"
    },
    {
        "ceo_name": "Eric Dresdale",
        "employee_name": "Mosawar Jamshady",
        "email": "mosawar.jamshady@entrokeylabs.com"
    },
    {
        "ceo_name": "Sammy Deeb",
        "employee_name": "Logan Taylor",
        "email": "logan@mhpbrokerage.com"
    },
    {
        "ceo_name": "S. Jack Hu",
        "employee_name": "Kevin Chen",
        "email": "kevin.chen@ucr.edu"
    },
    {
        "ceo_name": "Julio Frenk",
        "employee_name": "Isabella Guzman",
        "email": "iguzman@ucla.edu"
    },
    {
        "ceo_name": "Edward Ipser",
        "employee_name": "Maia Le",
        "email": "mle@ipserlab.com"
    },
    {
        "ceo_name": "Michael I. Kotlikoff",
        "employee_name": "Jason Kim",
        "email": "kim@cornell.edu"
    },
    {
        "ceo_name": "Steve de Jong",
        "employee_name": "Jono Back",
        "email": "jonoback@vrify.com"
    },
    {
        "ceo_name": "Richard Muma",
        "employee_name": "Maurice Henderson",
        "email": "maurice.henderson@wichita.edu"
    },
    {
        "ceo_name": "Sophia Murphy",
        "employee_name": "Abiha Kashif",
        "email": "akashif@iatp.org"
    },
    {
        "ceo_name": "Samila El-Sayed",
        "employee_name": "Lawrence Sammour",
        "email": "lsammour@crossrealms.com"
    },
    {
        "ceo_name": "Jarred VanHorn",
        "employee_name": "Grace Everhart",
        "email": "grace.everhart@seedsofsuccess.us"
    },
    {
        "ceo_name": "Alexander Chapman",
        "employee_name": "Andi Vrapcani",
        "email": "a.vrapcani@alexanderchapmanltd.com"
    },
    {
        "ceo_name": "Cecil Harper",
        "employee_name": "Grady Gardner",
        "email": "ggardner@hrkcpa.com"
    },
    {
        "ceo_name": "Randy Wright",
        "employee_name": "Reuben Roberts",
        "email": "rroberts@wuft.org"
    },
    {
        "ceo_name": "Joseph E. Aoun",
        "employee_name": "Varana Navadiya",
        "email": "navadiya.v@northeastern.edu"
    },
    {
        "ceo_name": "Eric Appel, Lucas Derraugh",
        "employee_name": "Angela Chiang",
        "email": "angela@cornellappdev.com"
    },
    {
        "ceo_name": "Donald W. Landry",
        "employee_name": "Nimisha Sarkar",
        "email": "nsarkar@ufl.edu"
    },
    {
        "ceo_name": "William Tate",
        "employee_name": "Rashi Mukherjee",
        "email": "rashi.mukherjee@rutgers.edu"
    },
    {
        "ceo_name": "Howard Gillman",
        "employee_name": "Alyas Thomas",
        "email": "alyast@uci.edu"
    },
    {
        "ceo_name": "Darryll Pines",
        "employee_name": "Le-Nair Koffa",
        "email": "lkoffa@umd.edu"
    },
    {
        "ceo_name": "Giancarlo Bellini",
        "employee_name": "Stefano Polidori",
        "email": "spolidori@toiturestroisetoiles.com"
    },
    {
        "ceo_name": "Amil Khanzada",
        "employee_name": "Pooja Manjunatha",
        "email": "pooja.manjunatha@virufy.org"
    },
    {
        "ceo_name": "Christopher Roberts",
        "employee_name": "George C",
        "email": "george.c@auburn.edu"
    },
    {
        "ceo_name": "Domenico Grasso",
        "employee_name": "Ruhi Kulkarni",
        "email": "ruhik@umich.edu"
    },
    {
        "ceo_name": "Jim Brown",
        "employee_name": "Aaliyah Dawn",
        "email": "aaliyah.dawn@brownpacking.com"
    },
    {
        "ceo_name": "J Snider",
        "employee_name": "Daniel Leo",
        "email": "daniel@sniderconsultinggroup.com"
    },
    {
        "ceo_name": "Gail Kitsis",
        "employee_name": "Alivia Tran",
        "email": "alivia-tran@crazybowlsandwraps.com"
    },
    {
        "ceo_name": "Paul Alivisatos",
        "employee_name": "Margaret Jennings",
        "email": "mjennings@uchicago.edu"
    },
    {
        "ceo_name": "Rucha Khanolkar",
        "employee_name": "Sophia Yang",
        "email": "sophia@hackbeanpot.com"
    },
    {
        "ceo_name": "Brady See",
        "employee_name": "Madhu Prabhu",
        "email": "mprabhu@illinoisbusinesscouncil.com"
    },
    {
        "ceo_name": "Howard Gillman",
        "employee_name": "Hetal Patel",
        "email": "hpatel@uci.edu"
    },
    {
        "ceo_name": "Wally Budgell",
        "employee_name": "Robert King",
        "email": "robertking@norleegroup.com"
    },
    {
        "ceo_name": "Wade Rousse",
        "employee_name": "Daniel Pete",
        "email": "daniel@lsu.edu"
    },
    {
        "ceo_name": "Donald W. Landry",
        "employee_name": "Kian Hidalgo",
        "email": "kian.hidalgo@ufl.edu"
    },
    {
        "ceo_name": "Vishal Grover",
        "employee_name": "Kalp Soni",
        "email": "kalp.soni@smesync.com"
    },
    {
        "ceo_name": "Dave Fulcher",
        "employee_name": "Hyejin Lee",
        "email": "hlee@trinityseniorservices.org"
    },
    {
        "ceo_name": "Ángel Cabrera",
        "employee_name": "Shahd B",
        "email": "shahd.b@gatech.edu"
    },
    {
        "ceo_name": "Lee H. Roberts",
        "employee_name": "Ifeoma Obioha",
        "email": "iobioha@unc.edu"
    },
    {
        "ceo_name": "Vince Beresford",
        "employee_name": "Nash Ashur",
        "email": "nashur@dreamcenter.org"
    },
    {
        "ceo_name": "Darryll Pines",
        "employee_name": "Caleb Kang",
        "email": "ckang@umd.edu"
    },
    {
        "ceo_name": "Kevin D. Strain",
        "employee_name": "Kevin Baritua",
        "email": "kevin.baritua@sunlife.com"
    },
    {
        "ceo_name": "Kim Nelson",
        "employee_name": "Jason Schreiber",
        "email": "jschreiber@redchalk.com"
    },
    {
        "ceo_name": "Eric Appel, Lucas Derraugh",
        "employee_name": "Daniel Weiner",
        "email": "daniel@cornellappdev.com"
    },
    {
        "ceo_name": "Bruce Meighen",
        "employee_name": "Amy Hartmann",
        "email": "ahartmann@logansimpson.com"
    },
    {
        "ceo_name": "Michael I. Kotlikoff",
        "employee_name": "Rex Popick",
        "email": "popick@cornell.edu"
    },
    {
        "ceo_name": "Jeffrey D. Armstrong",
        "employee_name": "Sameer Nadeem",
        "email": "snadeem@calpoly.edu"
    },
    {
        "ceo_name": "Neeli Bendapudi",
        "employee_name": "Samshita Maram",
        "email": "samshita-maram@psu.edu"
    },
    {
        "ceo_name": "John Kim",
        "employee_name": "Matthew Merz",
        "email": "matthew@paraform.com"
    },
    {
        "ceo_name": "Chris Sestito",
        "employee_name": "Will Jedrzejczak",
        "email": "wjedrzejczak@hiddenlayer.com"
    },
    {
        "ceo_name": "Gary May",
        "employee_name": "Sathvik Parasa",
        "email": "sparasa@ucdavis.edu"
    },
    {
        "ceo_name": "Lachlan Murdoch",
        "employee_name": "Leo Munoz",
        "email": "leo.munoz@fox.com"
    },
    {
        "ceo_name": "Jeff Landry",
        "employee_name": "Robert Dyess",
        "email": "robert.dyess@la.gov"
    },
    {
        "ceo_name": "Daniel Lurie",
        "employee_name": "Rashik Adhikari",
        "email": "rashik.adhikari@sfgov.org"
    },
    {
        "ceo_name": "Donald W. Landry",
        "employee_name": "Giles Greene",
        "email": "gilesgreene@ufl.edu"
    },
    {
        "ceo_name": "Melissa Zaikos",
        "employee_name": "Elijah Green",
        "email": "egreen@intrinsicschools.org"
    },
    {
        "ceo_name": "Ray L. Watts",
        "employee_name": "Khadijah Owens",
        "email": "kowens@uab.edu"
    },
    {
        "ceo_name": "William Tate",
        "employee_name": "Chloe Tirino",
        "email": "chloe.tirino@rutgers.edu"
    },
    {
        "ceo_name": "Joseph Harroz",
        "employee_name": "Aryan Singh",
        "email": "asingh@ou.edu"
    },
    {
        "ceo_name": "Christopher Hillis",
        "employee_name": "Eric Afriyie Adu",
        "email": "eadu@itdrc.org"
    },
    {
        "ceo_name": "Suresh Garimella",
        "employee_name": "Shreya Ardeshna",
        "email": "shreya@arizona.edu"
    },
    {
        "ceo_name": "Mark Shaw",
        "employee_name": "Tom Cruz",
        "email": "tcruz@sonatech.com"
    },
    {
        "ceo_name": "Craig Sheldon",
        "employee_name": "Trevion Collins",
        "email": "tcollins@cityofsherwood.net"
    },
    {
        "ceo_name": "Jonathan Levin",
        "employee_name": "Owen Luo",
        "email": "owenl@stanford.edu"
    },
    {
        "ceo_name": "Sam Oshay",
        "employee_name": "Jacob Appelbaum",
        "email": "jacob@recurrency.com"
    },
    {
        "ceo_name": "Terry Emery",
        "employee_name": "Connor Zehnder",
        "email": "czehnder@marysvilleohio.org"
    },
    {
        "ceo_name": "John Sackett",
        "employee_name": "Pia Alday",
        "email": "palday@adventisthealthcare.com"
    },
    {
        "ceo_name": "Michael Cvitkovic",
        "employee_name": "Corey Jean",
        "email": "cjean@abilitiescentre.org"
    },
    {
        "ceo_name": "Mike Wills",
        "employee_name": "Brooke Jones",
        "email": "brooke.jones@apexorderpickup.com"
    },
    {
        "ceo_name": "Thomas M. Angelo",
        "employee_name": "Alyssa Watson",
        "email": "awatson@hbkcpa.com"
    },
    {
        "ceo_name": "Michael Coristine",
        "employee_name": "Oscar Dominguez",
        "email": "oscar@coristinelaw.ca"
    },
    {
        "ceo_name": "Michelle Loyd Thompson",
        "employee_name": "Alexa Kalhorn",
        "email": "alexa.kalhorn@cbh.com"
    },
    {
        "ceo_name": "Ronald Rochon",
        "employee_name": "Julissa Olmos",
        "email": "jolmos@fullerton.edu"
    },
    {
        "ceo_name": "Brad Staples",
        "employee_name": "Isabel Epistelomogi",
        "email": "iepistelomogi@apcoworldwide.com"
    },
    {
        "ceo_name": "Founder role",
        "employee_name": "Arjun Kapadia",
        "email": "akapadia@aokservices.org"
    },
    {
        "ceo_name": "Cindy Gouveia",
        "employee_name": "Leanne Gulmayo",
        "email": "leanne.gulmayo@sheridancollege.ca"
    },
    {
        "ceo_name": "Maurie McInnis",
        "employee_name": "Steven Schmidt",
        "email": "steven.schmidt@yale.edu"
    },
    {
        "ceo_name": "Lee H. Roberts",
        "employee_name": "Kristina Hmilj",
        "email": "khmilj@unc.edu"
    },
    {
        "ceo_name": "Robert Alfred Dowd",
        "employee_name": "Lorena Maher",
        "email": "lmaher@nd.edu"
    },
    {
        "ceo_name": "Janet Truncale",
        "employee_name": "Jocelyn Mcaliney",
        "email": "jocelyn.mcaliney@ey.com"
    },
    {
        "ceo_name": "Aydin Senkut",
        "employee_name": "Aarush Agarwal",
        "email": "aarush@felicis.com"
    },
    {
        "ceo_name": "Josh Thompson",
        "employee_name": "Nicholas M",
        "email": "nicholas@civicsunplugged.org"
    },
    {
        "ceo_name": "Joseph E. Aoun",
        "employee_name": "Benjamin Marler",
        "email": "benjamin.m@northeastern.edu"
    },
    {
        "ceo_name": "Michael Ellison",
        "employee_name": "Jack Copeland",
        "email": "jack@codepath.org"
    },
    {
        "ceo_name": "Elizabeth Cantwell",
        "employee_name": "Sia C",
        "email": "sia.c@wsu.edu"
    },
    {
        "ceo_name": "Pete McCanna",
        "employee_name": "Aileen Nguyen",
        "email": "aileen.nguyen@bswhealth.com"
    },
    {
        "ceo_name": "Thomas Martucci",
        "employee_name": "Christy Ramage",
        "email": "cramage@themartuccigroup.com"
    },
    {
        "ceo_name": "Kurt M. Marisa",
        "employee_name": "Carter Marisa",
        "email": "carter@humandomainsolutions.us"
    },
    {
        "ceo_name": "James Davis",
        "employee_name": "Helen Chen",
        "email": "helen@utexas.edu"
    },
    {
        "ceo_name": "Boris Poludo",
        "employee_name": "Lucy Nwuneli",
        "email": "lnwuneli@canadianctb.ca"
    },
    {
        "ceo_name": "James Davis",
        "employee_name": "Neha Mathew",
        "email": "neha@utexas.edu"
    },
    {
        "ceo_name": "Pamela Whitten",
        "employee_name": "Allison Mercer",
        "email": "allison@indiana.edu"
    },
    {
        "ceo_name": "Dean Krech",
        "employee_name": "Jack Pectol",
        "email": "jack.p@jhmcpa.com"
    },
    {
        "ceo_name": "Gregory Williams",
        "employee_name": "Chris Tovar",
        "email": "ctovar@odessa.edu"
    },
    {
        "ceo_name": "Robert Alfred Dowd",
        "employee_name": "Madeleine Phan",
        "email": "mphan@nd.edu"
    },
    {
        "ceo_name": "Michael Sutton",
        "employee_name": "Elisa Yan",
        "email": "elisa@runtime.vc"
    },
    {
        "ceo_name": "Darryll Pines",
        "employee_name": "Sophia Portillo",
        "email": "sportillo@umd.edu"
    },
    {
        "ceo_name": "James Davis",
        "employee_name": "Madison Quach",
        "email": "madisonquach@utexas.edu"
    },
    {
        "ceo_name": "Jeanette Nuñez",
        "employee_name": "Shilat Jayo-Acuna",
        "email": "sjayo-acuna@fiu.edu"
    },
    {
        "ceo_name": "Joseph E. Aoun",
        "employee_name": "Salma Sheikh",
        "email": "sheikh.s@northeastern.edu"
    },
    {
        "ceo_name": "Alan Garber",
        "employee_name": "Allison Zhang",
        "email": "allison_zhang@harvard.edu"
    },
    {
        "ceo_name": "Rohan Sharma",
        "employee_name": "Eva Yentsch",
        "email": "eyentsch@nobenational.org"
    },
    {
        "ceo_name": "Richard Lyons",
        "employee_name": "Isabel X",
        "email": "isabel@berkeley.edu"
    },
    {
        "ceo_name": "Moez Limayem",
        "employee_name": "Andrew Chettipally",
        "email": "achettipally@usf.edu"
    },
    {
        "ceo_name": "Niels Valentiner",
        "employee_name": "Alex Stavron",
        "email": "astavron@vcbo.com"
    },
    {
        "ceo_name": "Franklin Gilliam",
        "employee_name": "Akshitha Kaleru",
        "email": "a_kaleru@uncg.edu"
    },
    {
        "ceo_name": "Reginald DesRoches",
        "employee_name": "Daniel J",
        "email": "daniel@rice.edu"
    },
    {
        "ceo_name": "Andy King",
        "employee_name": "Joseph Villa",
        "email": "jvilla@advantax.com"
    },
    {
        "ceo_name": "Ben Quiring",
        "employee_name": "Morgan Parent",
        "email": "mparent@quiring.com"
    },
    {
        "ceo_name": "James Davis",
        "employee_name": "Aaron Hu",
        "email": "aaron@utexas.edu"
    },
    {
        "ceo_name": "Madeleine Kaptein",
        "employee_name": "Curran A",
        "email": "ca@middleburycampus.com"
    },
    {
        "ceo_name": "Karina Kadia",
        "employee_name": "Ella Forkin",
        "email": "ella.forkin@hilltopconsultants.org"
    },
    {
        "ceo_name": "Patrice Sutton",
        "employee_name": "Tracey Aldred",
        "email": "taldred@lakecountyil.gov"
    },
    {
        "ceo_name": "Robert Alfred Dowd",
        "employee_name": "Mackenzie Cote",
        "email": "mcote@nd.edu"
    },
    {
        "ceo_name": "Elizabeth Guneratne",
        "employee_name": "Chloe Lorraine Talaugon",
        "email": "ctalaugon@moreaucatholic.org"
    },
    {
        "ceo_name": "Joseph E. Aoun",
        "employee_name": "Catherine Gore",
        "email": "gore.c@northeastern.edu"
    },
    {
        "ceo_name": "Vivek Goel",
        "employee_name": "Santosh Erathasari",
        "email": "serathasari@uwaterloo.ca"
    },
    {
        "ceo_name": "Coran Capshaw",
        "employee_name": "Caleb Irwin",
        "email": "caleb.irwin@redlightmanagement.com"
    },
    {
        "ceo_name": "William C. Dudley",
        "employee_name": "Wyatt Mayberry",
        "email": "mayberryw@wlu.edu"
    },
    {
        "ceo_name": "Pradeep Khosla",
        "employee_name": "Ji Ung Moon",
        "email": "jmoon@ucsd.edu"
    },
    {
        "ceo_name": "Jiachen He",
        "employee_name": "Syed Afnan Adit",
        "email": "aditsyed@affine.pro"
    },
    {
        "ceo_name": "Traci Donahue",
        "employee_name": "Nicholas Kline",
        "email": "nkline@crossvalleyfcu.org"
    },
    {
        "ceo_name": "Jenny Wang",
        "employee_name": "Ynalois Pangilinan",
        "email": "ynalois@altadaily.com"
    },
    {
        "ceo_name": "Dennis Assanis",
        "employee_name": "Mitalee Pasricha",
        "email": "mitaleepasricha@ucsb.edu"
    },
    {
        "ceo_name": "Thomas Savino",
        "employee_name": "Alexya Mendez",
        "email": "amendez@prospanica.org"
    },
    {
        "ceo_name": "Pete Barr",
        "employee_name": "Julia Bernstein",
        "email": "julia.bernstein@andbarr.co"
    },
    {
        "ceo_name": "Vince Bruni-Bossio",
        "employee_name": "Rutik Isai",
        "email": "rutik.isai@usask.ca"
    },
    {
        "ceo_name": "Gregory Crawford",
        "employee_name": "Nicholas Conlan",
        "email": "nicholas.conlan@miamioh.edu"
    },
    {
        "ceo_name": "Henry Bienen",
        "employee_name": "Hannah Webb",
        "email": "hannah@northwestern.edu"
    },
    {
        "ceo_name": "Katherine P. Frank",
        "employee_name": "Joel Adefrid",
        "email": "adefridj@uwstout.edu"
    },
    {
        "ceo_name": "Vincent Price",
        "employee_name": "Samuel E",
        "email": "samuel.e@duke.edu"
    },
    {
        "ceo_name": "Richard Lyons",
        "employee_name": "Aayan Rizvi",
        "email": "aayan@berkeley.edu"
    },
    {
        "ceo_name": "Julian Herzing-Burkard",
        "employee_name": "Aaniya Mahajan",
        "email": "aaniya.mahajan@northeasternsga.com"
    },
    {
        "ceo_name": "David Kaufman",
        "employee_name": "Matthew Cowan",
        "email": "mcowan@cuair.org"
    },
    {
        "ceo_name": "Richard Lyons",
        "employee_name": "Amber Yu",
        "email": "ayu@berkeley.edu"
    },
    {
        "ceo_name": "Kurtis Leinweber",
        "employee_name": "Ryan Vu",
        "email": "ryan.vu@ffca-calgary.com"
    },
    {
        "ceo_name": "Will Aarsheim",
        "employee_name": "Yovanny S",
        "email": "yovanny@missionbrain.org"
    },
    {
        "ceo_name": "Ángel Cabrera",
        "employee_name": "Agastya Kalagarla",
        "email": "agastya.kalagarla@gatech.edu"
    },
    {
        "ceo_name": "Moisés Kaufman",
        "employee_name": "Katie Wagner",
        "email": "katie@tectonictheaterproject.org"
    },
    {
        "ceo_name": "Danielle R. Holley",
        "employee_name": "Mary Grahn",
        "email": "mary-grahn@mtholyoke.edu"
    },
    {
        "ceo_name": "Roderick Ejuetami",
        "employee_name": "Elsie Ahachi",
        "email": "elsie@deedsmag.com"
    },
    {
        "ceo_name": "Kelli Walters",
        "employee_name": "Kaylie Avery Lichtenberger",
        "email": "kaylie@wtalentnyc.com"
    },
    {
        "ceo_name": "Sarah Scher",
        "employee_name": "John Ziouras",
        "email": "jziouras@capphysicians.com"
    },
    {
        "ceo_name": "Ellen Granberg",
        "employee_name": "Tess Rosler",
        "email": "tess.rosler@gwu.edu"
    },
    {
        "ceo_name": "General Manager of phl.com",
        "employee_name": "Melanie Ascoli",
        "email": "mascoli@phl17.com"
    },
    {
        "ceo_name": "Ángel Cabrera",
        "employee_name": "Raelyn Bailey",
        "email": "raelyn.bailey@gatech.edu"
    },
    {
        "ceo_name": "Marion Lieser",
        "employee_name": "Ella Peterson",
        "email": "e.peterson@light-for-the-world.org"
    },
    {
        "ceo_name": "Ender Korkmaz",
        "employee_name": "Jacob Lyons",
        "email": "jacob.lyons@heat.com"
    },
    {
        "ceo_name": "Patricia Carey",
        "employee_name": "Sara-James Ranta",
        "email": "sranta@alligator.org"
    },
    {
        "ceo_name": "Kin-Man Lee",
        "employee_name": "Caroline De Leon",
        "email": "caroline@fashionmagazine.com"
    },
    {
        "ceo_name": "Steve Raab",
        "employee_name": "Grace Mccarron",
        "email": "gmccarron@sny.tv"
    },
    {
        "ceo_name": "Beong-Soo Kim",
        "employee_name": "Yash Gupta",
        "email": "yash.gupta@usc.edu"
    },
    {
        "ceo_name": "Elon Musk",
        "employee_name": "Paulina Marcos",
        "email": "paulina-marcos@x.com"
    },
    {
        "ceo_name": "Timothy Sands",
        "employee_name": "Paula Ramos",
        "email": "paula@vt.edu"
    },
    {
        "ceo_name": "Ann Jordan",
        "employee_name": "Nikhil Idnani",
        "email": "nidnani@hfma.org"
    },
    {
        "ceo_name": "Paul Alivisatos",
        "employee_name": "Stella Chae",
        "email": "stella@uchicago.edu"
    },
    {
        "ceo_name": "Henry Bienen",
        "employee_name": "Chelsea Cain",
        "email": "chelsea.cain@northwestern.edu"
    },
    {
        "ceo_name": "Andrew McKeough",
        "employee_name": "Grace Sawyer",
        "email": "grace.sawyer@aksm.org"
    },
    {
        "ceo_name": "Mung Chiang",
        "employee_name": "Jessa Caffee",
        "email": "jcaffee@purdue.edu"
    },
    {
        "ceo_name": "Tony Montero",
        "employee_name": "Sean Edwards",
        "email": "sedwards@haihospitality.com"
    },
    {
        "ceo_name": "John Morayniss",
        "employee_name": "Ava Domenichelli",
        "email": "adomenichelli@blink49.com"
    },
    {
        "ceo_name": "Monica Lam",
        "employee_name": "Isaiah Rivera",
        "email": "irivera@dailycal.org"
    },
    {
        "ceo_name": "Elon Musk",
        "employee_name": "Jasmine M",
        "email": "jasmine-m@x.com"
    },
    {
        "ceo_name": "James Davis",
        "employee_name": "Evelyn Becerra",
        "email": "evelyn@utexas.edu"
    },
    {
        "ceo_name": "Joseph James Echevarria",
        "employee_name": "Brian Matute",
        "email": "b.matute@miami.edu"
    },
    {
        "ceo_name": "Chuck Singleton",
        "employee_name": "Eleanor Kinney",
        "email": "ekinney@wfuv.org"
    },
    {
        "ceo_name": "James Pitaro",
        "employee_name": "Alan Williams",
        "email": "alan.williams@espn.com"
    },
    {
        "ceo_name": "Robert Reffkin",
        "employee_name": "Eric Hardman",
        "email": "eric.hardman@compass.com"
    },
    {
        "ceo_name": "Richard Lyons",
        "employee_name": "Gina Storniolo",
        "email": "ginastorniolo@berkeley.edu"
    },
    {
        "ceo_name": "Elon Musk",
        "employee_name": "Ashly L",
        "email": "ashly-l@x.com"
    },
    {
        "ceo_name": "John Fry",
        "employee_name": "Molly Caufield",
        "email": "molly.caufield@temple.edu"
    },
    {
        "ceo_name": "Elon Musk",
        "employee_name": "Angela Rodriguez",
        "email": "angela-rodriguez@x.com"
    },
    {
        "ceo_name": "Anthony Casalena",
        "employee_name": "Sofia Richter",
        "email": "sofiarichter@squarespace.com"
    },
    {
        "ceo_name": "Beong-Soo Kim",
        "employee_name": "Andrés Chamorro Domenech",
        "email": "andres.domenech@usc.edu"
    },
    {
        "ceo_name": "James Casey",
        "employee_name": "Molly Solarsh",
        "email": "molly-solarsh@ups.com"
    },
    {
        "ceo_name": "Neeli Bendapudi",
        "employee_name": "Grace Decker",
        "email": "grace-decker@psu.edu"
    },
    {
        "ceo_name": "Erika Beck",
        "employee_name": "Emma S",
        "email": "emma.s@csun.edu"
    },
    {
        "ceo_name": "Monica Lam",
        "employee_name": "Siena Rangel",
        "email": "srangel@dailycal.org"
    },
    {
        "ceo_name": "Paula Kerger",
        "employee_name": "Sophie Luo",
        "email": "sophie@pbs.org"
    },
    {
        "ceo_name": "Rita Forden",
        "employee_name": "Isaac Gollapalli",
        "email": "igollapalli@aof.org"
    },
    {
        "ceo_name": "Justin Wineburgh",
        "employee_name": "Chloe Goldstein",
        "email": "cgoldstein@alkemy-x.com"
    },
    {
        "ceo_name": "Steve Hodgetts",
        "employee_name": "Joshua Gray",
        "email": "joshua@annabarb.com"
    },
    {
        "ceo_name": "Chris Locke",
        "employee_name": "Emma Schneider",
        "email": "emma@unlockethelight.com"
    },
    {
        "ceo_name": "Jeff Cavignac",
        "employee_name": "Jake Pearlman",
        "email": "jpearlman@cavignac.com"
    },
    {
        "ceo_name": "Beong-Soo Kim",
        "employee_name": "Azam Modan",
        "email": "azam.modan@usc.edu"
    },
    {
        "ceo_name": "John Fry",
        "employee_name": "Mia Zayas",
        "email": "mia@temple.edu"
    },
    {
        "ceo_name": "Linda G. Mills",
        "employee_name": "Daisy D",
        "email": "daisy.d@nyu.edu"
    },
    {
        "ceo_name": "Ari Nisman",
        "employee_name": "Jarred Weisfelner",
        "email": "jarred.weisfelner@degy.com"
    },
    {
        "ceo_name": "Monica Lam",
        "employee_name": "Amanda Mcleod",
        "email": "amcleod@dailycal.org"
    },
    {
        "ceo_name": "John Fry",
        "employee_name": "Anthony Roscioli",
        "email": "anthony.roscioli@temple.edu"
    },
    {
        "ceo_name": "Joseph Harroz",
        "employee_name": "Andrew Paredes",
        "email": "aparedes@ou.edu"
    },
    {
        "ceo_name": "David Kirchhoff",
        "employee_name": "Chase Vaughn",
        "email": "chasev@worldstrides.com"
    },
    {
        "ceo_name": "Enrique Abeyta",
        "employee_name": "Dimitry Mak",
        "email": "mak@revolvermag.com"
    },
    {
        "ceo_name": "Alan Garber",
        "employee_name": "Priya Allen",
        "email": "priya_allen@harvard.edu"
    },
    {
        "ceo_name": "La Jerne Terry Cornish",
        "employee_name": "Morgan Moracco",
        "email": "mmoracco@ithaca.edu"
    },
    {
        "ceo_name": "Beong-Soo Kim",
        "employee_name": "Julian Gajewski",
        "email": "julian.gajewski@usc.edu"
    },
    {
        "ceo_name": "Perry A. Sook",
        "employee_name": "Nina Gallegos",
        "email": "ngallegos@ktsm.com"
    },
    {
        "ceo_name": "Linda G. Mills",
        "employee_name": "Anna R",
        "email": "anna.r@nyu.edu"
    },
    {
        "ceo_name": "Marcelo Alquezar",
        "employee_name": "María Alquezar",
        "email": "malquezar@gsabpo.com"
    },
    {
        "ceo_name": "Henry Bienen",
        "employee_name": "Jack Ververis",
        "email": "jack.ververis@northwestern.edu"
    },
    {
        "ceo_name": "Robert Stromberg",
        "employee_name": "John Michael Symington",
        "email": "john@secretcity.studio"
    },
    {
        "ceo_name": "Chuck Singleton",
        "employee_name": "Diana Juarez",
        "email": "djuarez@wfuv.org"
    },
    {
        "ceo_name": "Nicole Bulanchuk",
        "employee_name": "Bryan Zhao",
        "email": "bryan@believeny.org"
    },
    {
        "ceo_name": "Alex Reneman",
        "employee_name": "Asher Smith",
        "email": "asher.smith@mountainleverage.com"
    },
    {
        "ceo_name": "Raoul Davis",
        "employee_name": "Jenica Jenkins",
        "email": "jenica.jenkins@ascendantgroupbranding.com"
    },
    {
        "ceo_name": "Tommy Ostendorf",
        "employee_name": "Jason Cooney-Cordero",
        "email": "jcooney-cordero@beachsports.com"
    },
    {
        "ceo_name": "Danny Lerner",
        "employee_name": "Carlos Erquiaga",
        "email": "cerquiaga@millennium-media.net"
    },
    {
        "ceo_name": "Christina Paxson",
        "employee_name": "Marta Jurzyk",
        "email": "marta_jurzyk@brown.edu"
    },
    {
        "ceo_name": "Klaus-Peter Schulenberg",
        "employee_name": "Chloé Fernando-English",
        "email": "chloe.fernando-english@eventimapollo.com"
    },
    {
        "ceo_name": "Reaghan Chen",
        "employee_name": "Chloe Bradley",
        "email": "cbradley@kykernel.com"
    },
    {
        "ceo_name": "Daniel Joseph Clancy",
        "employee_name": "Macey Horton",
        "email": "macey.horton@twitch.tv"
    },
    {
        "ceo_name": "Joseph Harroz",
        "employee_name": "Kayla Reinick",
        "email": "kreinick@ou.edu"
    },
    {
        "ceo_name": "Kimberly Palmer",
        "employee_name": "Dylan Ricci",
        "email": "dricci@newportfilm.com"
    },
    {
        "ceo_name": "Laura A. Carlson",
        "employee_name": "Soph Sobota",
        "email": "ssobota@udel.edu"
    },
    {
        "ceo_name": "Jon Glass",
        "employee_name": "Jack Henry",
        "email": "jack.henry@thenewshouse.com"
    },
    {
        "ceo_name": "Pradeep Khosla",
        "employee_name": "Jean Paul Mhanna",
        "email": "jmhanna@ucsd.edu"
    },
    {
        "ceo_name": "Stacy Milner",
        "employee_name": "Kendall Johnson",
        "email": "kendall@eicop.org"
    },
    {
        "ceo_name": "Amelia Fortgang, Erika Tam",
        "employee_name": "Padma Balaji",
        "email": "padma@baycs.org"
    },
    {
        "ceo_name": "Alex Cooper",
        "employee_name": "Emma Welty",
        "email": "emma@iamunwell.com"
    },
    {
        "ceo_name": "Eric Clark",
        "employee_name": "Matthews Farias",
        "email": "mfarias@manh.com"
    },
    {
        "ceo_name": "Anthony Casalena",
        "employee_name": "Zoe Boxenbaum",
        "email": "zoeboxenbaum@squarespace.com"
    },
    {
        "ceo_name": "Derek Jones",
        "employee_name": "Jake Kitchin",
        "email": "jake@rowanradio.com"
    },
    {
        "ceo_name": "Vivienne Francis",
        "employee_name": "Juliet Seith",
        "email": "juliet@oneworldmedia.org.uk"
    },
    {
        "ceo_name": "Jay McCloskey",
        "employee_name": "Aiden Mccloskey",
        "email": "aiden@trustsynergy.com"
    },
    {
        "ceo_name": "Mark Braly",
        "employee_name": "Emma Mcmurrough",
        "email": "emma@bralyinsurance.com"
    },
    {
        "ceo_name": "Cheralyn Chok",
        "employee_name": "Ella Gaspar",
        "email": "ella.gaspar@propelimpact.com"
    },
    {
        "ceo_name": "Henry Bienen",
        "employee_name": "Katarzyna Nguyen",
        "email": "katarzyna.nguyen@northwestern.edu"
    },
    {
        "ceo_name": "Kent Syverud",
        "employee_name": "Jnana Velamuri",
        "email": "jvelamuri@syr.edu"
    },
    {
        "ceo_name": "David Fischer",
        "employee_name": "Nyla Moxley",
        "email": "nmoxley@knkx.org"
    },
    {
        "ceo_name": "Beong-Soo Kim",
        "employee_name": "Maximus Patri",
        "email": "maximus.patri@usc.edu"
    },
    {
        "ceo_name": "Peter Harris",
        "employee_name": "Robert Pyles",
        "email": "rpyles@ugrowthfund.com"
    },
    {
        "ceo_name": "William Tate",
        "employee_name": "Makali Pennycooke",
        "email": "makali.pennycooke@rutgers.edu"
    },
    {
        "ceo_name": "Stacy Milner",
        "employee_name": "Imani Mullings",
        "email": "imani@eicop.org"
    },
    {
        "ceo_name": "Robert Kaplan",
        "employee_name": "Ronan Azzam",
        "email": "razzam@upennsfcu.org"
    },
    {
        "ceo_name": "Bill Horgan",
        "employee_name": "Jaiden Dumont",
        "email": "jaiden@debugpestcontrol.com"
    },
    {
        "ceo_name": "Beong-Soo Kim",
        "employee_name": "Abir Bhatt",
        "email": "abir.bhatt@usc.edu"
    },
    {
        "ceo_name": "Sal Marini",
        "employee_name": "Faith Marini",
        "email": "fmarini@aecare911.org"
    },
    {
        "ceo_name": "Patrick Walker",
        "employee_name": "Mckenna Elinski",
        "email": "mckenna@3ptproductions.com"
    },
    {
        "ceo_name": "Henry Bienen",
        "employee_name": "Victoria Ryan",
        "email": "victoria.ryan@northwestern.edu"
    },
    {
        "ceo_name": "Josh Bishop",
        "employee_name": "Jaiden Louden",
        "email": "jlouden@stn2.tv"
    },
    {
        "ceo_name": "David Zaslav",
        "employee_name": "Bona S",
        "email": "sb@wbd.com"
    },
    {
        "ceo_name": "Beong-Soo Kim",
        "employee_name": "Chelsea Z",
        "email": "chelseaz@usc.edu"
    },
    {
        "ceo_name": "Randy Larsen",
        "employee_name": "Dominik Lettovsky",
        "email": "dominik.lettovsky@assuredpartners.com"
    },
    {
        "ceo_name": "Paula Johnson",
        "employee_name": "Yuchen Xiao",
        "email": "yuchen.xiao@wellesley.edu"
    },
    {
        "ceo_name": "Penn chapter",
        "employee_name": "Isabella Raffo Pedraza",
        "email": "isabella@hack4impact.org"
    },
    {
        "ceo_name": "Joseph E. Aoun",
        "employee_name": "Molly Forman",
        "email": "m.forman@northeastern.edu"
    },
    {
        "ceo_name": "Calaf Nuances",
        "employee_name": "Ethan Arteaga",
        "email": "ethan.a@calaaf.com"
    },
    {
        "ceo_name": "Robert Alan Iger",
        "employee_name": "Mia Goldstein",
        "email": "mia.goldstein@disney.com"
    },
    {
        "ceo_name": "Rishabh Meswani",
        "employee_name": "Kanak Panigrahi",
        "email": "kanak@fremontdebateacademy.org"
    },
    {
        "ceo_name": "Steven Schneider",
        "employee_name": "Brian Liu",
        "email": "bliu@professionalpt.com"
    },
    {
        "ceo_name": "Michael Grosse",
        "employee_name": "Yaning Hu",
        "email": "yaning.hu@sartorius.com"
    },
    {
        "ceo_name": "Larry R. Thompson",
        "employee_name": "Martina Belanche Castillo",
        "email": "mcastillo@ringling.edu"
    },
    {
        "ceo_name": "Madison Semarjian",
        "employee_name": "Amanda Chan",
        "email": "amandachan@themadaapp.com"
    },
    {
        "ceo_name": "P. Barry Butler",
        "employee_name": "Alexandra Olaes",
        "email": "alexandra.olaes@erau.edu"
    },
    {
        "ceo_name": "Dhiman Bhattacharjee",
        "employee_name": "Tara Khambadkone",
        "email": "tara@finexusinc.ai"
    },
    {
        "ceo_name": "Obi Omile",
        "employee_name": "Valentine Nwachukwu",
        "email": "valentine@thecut.co"
    },
    {
        "ceo_name": "Douglas Girod",
        "employee_name": "Bridget Connelly",
        "email": "bridget.connelly@ku.edu"
    },
    {
        "ceo_name": "Joseph E. Aoun",
        "employee_name": "Jolin Huang",
        "email": "huang.j@northeastern.edu"
    },
    {
        "ceo_name": "Satya Nadella",
        "employee_name": "Chuer Yang",
        "email": "yangc@microsoft.com"
    },
    {
        "ceo_name": "Clincy Cheung",
        "employee_name": "David Yen",
        "email": "david@dropletpharma.com"
    },
    {
        "ceo_name": "Tim Scott",
        "employee_name": "Evelyn Huang",
        "email": "ehuang@biocom.org"
    },
    {
        "ceo_name": "Beong-Soo Kim",
        "employee_name": "Julia Mao",
        "email": "julia.mao@usc.edu"
    },
    {
        "ceo_name": "Matt Fults",
        "employee_name": "David Hasslinger",
        "email": "dhasslinger@epinc.com"
    },
    {
        "ceo_name": "Robert Marshall",
        "employee_name": "Mariel Miranda",
        "email": "mmiranda@driabilene.org"
    },
    {
        "ceo_name": "Michael I. Kotlikoff",
        "employee_name": "Charlotte Li",
        "email": "li@cornell.edu"
    },
    {
        "ceo_name": "Cady Short-Thompson",
        "employee_name": "Emily Belcher",
        "email": "emily@nku.edu"
    },
    {
        "ceo_name": "Vlatko Demrovski",
        "employee_name": "Carissa Ott",
        "email": "carissa@elementkb.com"
    },
    {
        "ceo_name": "Dov Yoran",
        "employee_name": "Ashley Yang",
        "email": "ashley@cmdzero.io"
    },
    {
        "ceo_name": "Rusty Hale",
        "employee_name": "Angelica Mcclurkan",
        "email": "angelica.mcclurkan@halecpagroup.com"
    },
    {
        "ceo_name": "Tommy Smith",
        "employee_name": "Riley Smith",
        "email": "riley@ftlutd.com"
    },
    {
        "ceo_name": "Arthur Baranovskiy",
        "employee_name": "Keanna Keller",
        "email": "keanna@aryeng.com"
    },
    {
        "ceo_name": "Melissa L. Gilliam",
        "employee_name": "Kate Seo",
        "email": "kates@bu.edu"
    },
    {
        "ceo_name": "VACATIONS INC",
        "employee_name": "Michelle Moreno",
        "email": "mmoreno@ultimateresortvacations.com"
    },
    {
        "ceo_name": "Travis Scott",
        "employee_name": "Chad Washington",
        "email": "cwashington@cactipark.com"
    },
    {
        "ceo_name": "Glenn Meehan",
        "employee_name": "Isabel Baraff",
        "email": "isabel@evvyawards.org"
    },
    {
        "ceo_name": "Mung Chiang",
        "employee_name": "Nick Dalrymple",
        "email": "ndalrymple@purdue.edu"
    },
    {
        "ceo_name": "Georgina Shea",
        "employee_name": "Catherine Sipe",
        "email": "csipe@romanandwilliams.com"
    },
    {
        "ceo_name": "Richard Lyons",
        "employee_name": "Vincent Tang",
        "email": "vincent@berkeley.edu"
    },
    {
        "ceo_name": "Maurie McInnis",
        "employee_name": "Priscilla Barker",
        "email": "priscilla.barker@yale.edu"
    },
    {
        "ceo_name": "Edward Moydell",
        "employee_name": "Katie Linton",
        "email": "klinton@holdenfg.org"
    },
    {
        "ceo_name": "Vivek Goel",
        "employee_name": "Oliver Wang",
        "email": "owang@uwaterloo.ca"
    },
    {
        "ceo_name": "Jennifer Mnookin",
        "employee_name": "Ethan Pan",
        "email": "ethan.pan@wisc.edu"
    },
    {
        "ceo_name": "Suzanne Neal",
        "employee_name": "Vanessa Gonzales",
        "email": "vanessa@canyoncreative.org"
    },
    {
        "ceo_name": "Axel Hutapea",
        "employee_name": "Jessica Mailoa",
        "email": "jessicamailoa@permiasnasional.com"
    },
    {
        "ceo_name": "Alan Miller",
        "employee_name": "Griffin Weiss",
        "email": "griffin@officialleague.co"
    },
    {
        "ceo_name": "Beong-Soo Kim",
        "employee_name": "Mia Alonso",
        "email": "mia.alonso@usc.edu"
    },
    {
        "ceo_name": "Beong-Soo Kim",
        "employee_name": "Magen Mozeh",
        "email": "magen.mozeh@usc.edu"
    },
    {
        "ceo_name": "Jason Slocum",
        "employee_name": "Jessy Mancha",
        "email": "jmancha@i2gsystems.com"
    },
    {
        "ceo_name": "C. Mauli Agrawal",
        "employee_name": "Harryson Salcedo",
        "email": "harryson.salcedo@umkc.edu"
    },
    {
        "ceo_name": "William Ballard Hoyt",
        "employee_name": "Anjelina Gonzalez",
        "email": "agonzalez@cornellsun.com"
    },
    {
        "ceo_name": "Richard Christopher Murphy",
        "employee_name": "Zaven Kazandjian",
        "email": "zaven@bladeworkgames.com"
    },
    {
        "ceo_name": "Cindy Gouveia",
        "employee_name": "Natalie Kierpiec",
        "email": "natalie.kierpiec@sheridancollege.ca"
    },
    {
        "ceo_name": "Jay M. Bernhardt",
        "employee_name": "Kate Slade",
        "email": "kate_slade@emerson.edu"
    },
    {
        "ceo_name": "Domenico Grasso",
        "employee_name": "Abrar Shariff",
        "email": "shariff@umich.edu"
    },
    {
        "ceo_name": "Travis Wiltshire",
        "employee_name": "Alejandro Sanchez",
        "email": "alejandro.sanchez@cngengineering.com"
    },
    {
        "ceo_name": "Ellen Granberg",
        "employee_name": "Sandra Koretz",
        "email": "sandrakoretz@gwu.edu"
    },
    {
        "ceo_name": "Anthony Olivas",
        "employee_name": "Matthew Broyles",
        "email": "matthew.broyles@vertenergygroup.com"
    },
    {
        "ceo_name": "Michael Crow",
        "employee_name": "Loren Mcclure",
        "email": "loren.mcclure@asu.edu"
    },
    {
        "ceo_name": "Nina Bouzamondo-Bernstein",
        "employee_name": "Precious Nwofor",
        "email": "preciousn@prehealthshadowing.com"
    },
    {
        "ceo_name": "Walter Carter",
        "employee_name": "Willow Kim",
        "email": "willow.kim@osu.edu"
    },
    {
        "ceo_name": "Barton Rogers",
        "employee_name": "Luke Sylvester",
        "email": "luke@mit.edu"
    },
    {
        "ceo_name": "Daniel Lenefsky",
        "employee_name": "Kesav Rao",
        "email": "kesav@aspirefundingplatform.com"
    },
    {
        "ceo_name": "Matt Narus",
        "employee_name": "Violet Oconnell",
        "email": "voconnell@konaengineering.com"
    },
    {
        "ceo_name": "Andrew Qian, Cynthia Lan",
        "employee_name": "Nadia Choophungart",
        "email": "nadia@cornelldti.org"
    },
    {
        "ceo_name": "Andrea Colagrande",
        "employee_name": "Tanya Jain",
        "email": "tanya@foundstudy.com"
    },
    {
        "ceo_name": "Gart Davis",
        "employee_name": "Emily Woodard",
        "email": "ewoodard@spoonflower.com"
    },
    {
        "ceo_name": "Kelly Zhou",
        "employee_name": "Annie Li",
        "email": "annie.li@hackutd.co"
    },
    {
        "ceo_name": "Kevin Guskiewicz",
        "employee_name": "Eliza Delwiche",
        "email": "delwichee@msu.edu"
    },
    {
        "ceo_name": "Jacob Martinez",
        "employee_name": "Fatima Perez",
        "email": "fperez@digitalnest.org"
    },
    {
        "ceo_name": "Deep Saini",
        "employee_name": "Nina Howell",
        "email": "nina.howell@mcgill.ca"
    },
    {
        "ceo_name": "Bob Bursey",
        "employee_name": "Evelyn Becerra",
        "email": "ebecerra@texasperformingarts.org"
    },
    {
        "ceo_name": "Jason Brummond",
        "employee_name": "Ana Rivera",
        "email": "ana.rivera@dailyiowan.com"
    },
    {
        "ceo_name": "Joe Mansueto",
        "employee_name": "Serena Cai",
        "email": "scai@mansueto.com"
    },
    {
        "ceo_name": "Kimo Ah Yun",
        "employee_name": "Daniel Sineni",
        "email": "daniel.sineni@mu.edu"
    },
    {
        "ceo_name": "Mary Zhu",
        "employee_name": "Naya Hair",
        "email": "naya.hair@developforgood.org"
    },
    {
        "ceo_name": "Jeffrey L. Powell",
        "employee_name": "Ivan Guo",
        "email": "ivan.guo@kadant.com"
    },
    {
        "ceo_name": "Brian Barninger",
        "employee_name": "Brandon Kho",
        "email": "bkho@bel-eng.com"
    },
    {
        "ceo_name": "Katia Passerini",
        "employee_name": "Sarah Prentice",
        "email": "prentice@gonzaga.edu"
    },
    {
        "ceo_name": "Rockwell Shah",
        "employee_name": "Joel Awuku-Asante",
        "email": "joel.awuku-asante@ozlosleep.com"
    },
    {
        "ceo_name": "Stacia G Campbell",
        "employee_name": "Laura Horne",
        "email": "l.horne@dailynorthwestern.com"
    },
    {
        "ceo_name": "Julie Porter",
        "employee_name": "Melissa Chible",
        "email": "melissa@itsfrontporch.com"
    },
    {
        "ceo_name": "Michael Drizake",
        "employee_name": "Xavier Crystian",
        "email": "xavier@pitgranite.com"
    },
    {
        "ceo_name": "Michael I. Kotlikoff",
        "employee_name": "Andrew Wheat",
        "email": "wheat@cornell.edu"
    },
    {
        "ceo_name": "Dean Herbert",
        "employee_name": "Kyle Zhao",
        "email": "kyle@ppy.sh"
    },
    {
        "ceo_name": "Hannah Limary",
        "employee_name": "Angie Xetey",
        "email": "angie@designatuci.com"
    },
    {
        "ceo_name": "Jenny Cross",
        "employee_name": "Jackson Adams",
        "email": "jackson@twotonecreative.com"
    },
    {
        "ceo_name": "Neeli Bendapudi",
        "employee_name": "Devanshi Gupta",
        "email": "devanshi-gupta@psu.edu"
    },
    {
        "ceo_name": "Danny Coello",
        "employee_name": "Anna Cotter",
        "email": "anna.cotter@dial911fordesign.com"
    },
    {
        "ceo_name": "Cynthia Teniente-Matson",
        "employee_name": "Gianna Del Rosario",
        "email": "gianna.rosario@sjsu.edu"
    },
    {
        "ceo_name": "Aaron Hadley",
        "employee_name": "Sidney Shaffer",
        "email": "sshaffer@campbenfrankel.org"
    },
    {
        "ceo_name": "Steve Caloca",
        "employee_name": "Casandra Coleman",
        "email": "casandra.coleman@queenmary.com"
    },
    {
        "ceo_name": "Richard Lyons",
        "employee_name": "Abigail Wen",
        "email": "abigail@berkeley.edu"
    },
    {
        "ceo_name": "Olivia Trivisani Bowker",
        "employee_name": "Lydia Schubert",
        "email": "lydia.schubert@amivero.com"
    },
    {
        "ceo_name": "Jonathan Levin",
        "employee_name": "Aaira Goswami",
        "email": "aaira@stanford.edu"
    },
    {
        "ceo_name": "Richard Lyons",
        "employee_name": "Aashna Patel",
        "email": "patela@berkeley.edu"
    },
    {
        "ceo_name": "Joseph James Echevarria",
        "employee_name": "Izzi Guzman",
        "email": "i.guzman@miami.edu"
    },
    {
        "ceo_name": "Julia Harrod",
        "employee_name": "Nya Stringer",
        "email": "nstringer@mwm-arch.com"
    },
    {
        "ceo_name": "Brody Haar",
        "employee_name": "Katelyn Doanla",
        "email": "katelyn.doanla@productspace.org"
    },
    {
        "ceo_name": "Jason McClenahan",
        "employee_name": "Kelsey Brennan",
        "email": "kelsey.brennan@edealer.ca"
    },
    {
        "ceo_name": "Chase Edgelow",
        "employee_name": "Jack Xu",
        "email": "jack@evergeninfra.com"
    },
    {
        "ceo_name": "Ray Jones",
        "employee_name": "Reid Jones",
        "email": "reid@ravenmechanical.com"
    },
    {
        "ceo_name": "Michael Snopkowski",
        "employee_name": "Katelyn Davis",
        "email": "katelyn_davis@elanco.org"
    },
    {
        "ceo_name": "Viraja Gopisetty",
        "employee_name": "Aamani Cherukuri",
        "email": "aamani.cherukuri@frogforce503.org"
    },
    {
        "ceo_name": "Richard Lyons",
        "employee_name": "Karen Pham",
        "email": "pham@berkeley.edu"
    },
    {
        "ceo_name": "Jahanshah Nazmiyal",
        "employee_name": "Rishav K",
        "email": "rishav@rugandkilim.com"
    },
    {
        "ceo_name": "Anthony Sblendorio",
        "employee_name": "Alexandra Corman",
        "email": "acorman@backtonature.net"
    },
    {
        "ceo_name": "Penn chapter",
        "employee_name": "Angela T",
        "email": "angela@hack4impact.org"
    },
    {
        "ceo_name": "Yayoi Michimura",
        "employee_name": "Miku Tagaya",
        "email": "tagaya_miku@hugcome.co.jp"
    },
    {
        "ceo_name": "David Faulkenberry",
        "employee_name": "Sarah Hoffman Hilton",
        "email": "sarah@localboyoutfitters.com"
    },
    {
        "ceo_name": "Daniel Diermeier",
        "employee_name": "Miao Deng",
        "email": "miao.deng@vanderbilt.edu"
    },
    {
        "ceo_name": "Daniel Murphy",
        "employee_name": "Grace Hall",
        "email": "ghall@strategicfranchising.com"
    },
    {
        "ceo_name": "Michael I. Kotlikoff",
        "employee_name": "Keira He",
        "email": "he@cornell.edu"
    },
    {
        "ceo_name": "Ángel Cabrera",
        "employee_name": "David Renshaw",
        "email": "david.renshaw@gatech.edu"
    },
    {
        "ceo_name": "Neeli Bendapudi",
        "employee_name": "Rudra Desai",
        "email": "rudra-desai@psu.edu"
    },
    {
        "ceo_name": "Beong-Soo Kim",
        "employee_name": "Lauren Tonsich",
        "email": "lauren.tonsich@usc.edu"
    },
    {
        "ceo_name": "David Dunning",
        "employee_name": "Kaitlyn Allen",
        "email": "kallen@townofchili.org"
    },
    {
        "ceo_name": "Joseph E. Aoun",
        "employee_name": "Jade Hausmann",
        "email": "hausmann.j@northeastern.edu"
    },
    {
        "ceo_name": "Ryan Lo",
        "employee_name": "Jonathan Lee How Cheong",
        "email": "jonathancheong@urbanminds.co"
    },
    {
        "ceo_name": "Su Mathews Hale",
        "employee_name": "Kennedy Intihar",
        "email": "kennedy@hellohaledesign.com"
    },
    {
        "ceo_name": "Claire Yurkika Davis",
        "employee_name": "Rency Visperas",
        "email": "rency@hanger.life"
    },
    {
        "ceo_name": "Domenico Grasso",
        "employee_name": "Meera Boyapati",
        "email": "meerab@umich.edu"
    },
    {
        "ceo_name": "Nicholas Martin",
        "employee_name": "Ananda Feron",
        "email": "ananda@cgcg.biz"
    },
    {
        "ceo_name": "Trish Kelly",
        "employee_name": "Saanvi Bhat",
        "email": "sbhat@ecuad.ca"
    },
    {
        "ceo_name": "Lizzy Alspach",
        "employee_name": "Alexandra Burke",
        "email": "aburke@dbknews.com"
    },
    {
        "ceo_name": "Dave Lede",
        "employee_name": "Ali Idrissi",
        "email": "ali.idrissi@ledcor.com"
    },
    {
        "ceo_name": "Phil O'Neill",
        "employee_name": "Baran Kalayci",
        "email": "baran@omengineering.ca"
    },
    {
        "ceo_name": "Helge Seetzen",
        "employee_name": "Félix Hénard",
        "email": "felix.henard@tandemlaunch.com"
    },
    {
        "ceo_name": "Project Co-Lead",
        "employee_name": "Taha Esmahi",
        "email": "taha@arvp.org"
    },
    {
        "ceo_name": "Dylan Vidal",
        "employee_name": "Cheryl N",
        "email": "cheryl@knighthacks.org"
    },
    {
        "ceo_name": "Patricia Carey",
        "employee_name": "Del Halter",
        "email": "dhalter@alligator.org"
    },
    {
        "ceo_name": "Joseph Schumaker",
        "employee_name": "Joshua Murray",
        "email": "joshua@myfoodspace.com"
    },
    {
        "ceo_name": "Nishanth Bhargava",
        "employee_name": "Eunice Choi",
        "email": "choi@34st.com"
    },
    {
        "ceo_name": "Scott Stevenson",
        "employee_name": "Abeer Das",
        "email": "abeer.das@spellbook.legal"
    },
    {
        "ceo_name": "Cimin Cohen",
        "employee_name": "Jackson Pickett",
        "email": "jackson@ideapeddler.com"
    },
    {
        "ceo_name": "Jeff Crull",
        "employee_name": "Carl Sabroff",
        "email": "csabroff@credopd.com"
    },
    {
        "ceo_name": "James Davis",
        "employee_name": "Tyler Henry",
        "email": "tyler.henry@utexas.edu"
    },
    {
        "ceo_name": "Debra J. Thomas",
        "employee_name": "Kevin Allan",
        "email": "kallan@rockteach.org"
    },
    {
        "ceo_name": "Crystal Williams",
        "employee_name": "Yanyi Fu",
        "email": "yfu@risd.edu"
    },
    {
        "ceo_name": "Suzanne Sowinski",
        "employee_name": "Giovanni Ruiz",
        "email": "gruiz@sowinskisullivan.com"
    },
    {
        "ceo_name": "Gerard Downes",
        "employee_name": "Sarah Li",
        "email": "sarah.li@hexlabs.org"
    },
    {
        "ceo_name": "Matt Chambers",
        "employee_name": "Maria Pasyechnyk",
        "email": "mpasyechnyk@loxo.co"
    },
    {
        "ceo_name": "Sian Leah Beilock",
        "employee_name": "Vismaya Gopalan",
        "email": "vismaya.gopalan@dartmouth.edu"
    },
    {
        "ceo_name": "Steven McLaughlin",
        "employee_name": "Ifeoma Obioha",
        "email": "iobioha@cooper.edu"
    },
    {
        "ceo_name": "Rucha Khanolkar",
        "employee_name": "Annabelle C",
        "email": "annabelle@hackbeanpot.com"
    },
    {
        "ceo_name": "James Davis",
        "employee_name": "Audrey Kirwin",
        "email": "audrey@utexas.edu"
    },
    {
        "ceo_name": "Domenico Grasso",
        "employee_name": "Ava Sproull",
        "email": "asproull@umich.edu"
    },
    {
        "ceo_name": "David Stirling",
        "employee_name": "Justin Luu",
        "email": "justinluu@uwblueprint.org"
    },
    {
        "ceo_name": "Beong-Soo Kim",
        "employee_name": "Jaehyuk Choi",
        "email": "jaehyuk.choi@usc.edu"
    },
    {
        "ceo_name": "Kayleigh Bottomley",
        "employee_name": "Brent Mcvicker",
        "email": "brent.mcvicker@storm4.com"
    },
    {
        "ceo_name": "Ramit Varma",
        "employee_name": "Jarrod Wells",
        "email": "jarrod@breakoutlearning.com"
    },
    {
        "ceo_name": "Radenka Maric",
        "employee_name": "Anny Zheng",
        "email": "anny.zheng@uconn.edu"
    },
    {
        "ceo_name": "Patricia Carey",
        "employee_name": "Helen Alvarez",
        "email": "halvarez@alligator.org"
    },
    {
        "ceo_name": "Butch Terpening",
        "employee_name": "Abu Nazmurreza",
        "email": "anazmurreza@ct-eng.com"
    },
    {
        "ceo_name": "Duane Knickerbocker",
        "employee_name": "Adam Snyder",
        "email": "adams@browermechanical.com"
    },
    {
        "ceo_name": "Gauri Sreekumar",
        "employee_name": "Gauri Sreekumar",
        "email": "gauri@lawfer.in"
    },
    {
        "ceo_name": "Neeli Bendapudi",
        "employee_name": "Elizabeth Lovrak",
        "email": "elizabeth-lovrak@psu.edu"
    },
    {
        "ceo_name": "La Jerne Terry Cornish",
        "employee_name": "Lucia Iandolo",
        "email": "liandolo@ithaca.edu"
    },
    {
        "ceo_name": "Bill Maxson",
        "employee_name": "Cathryn Wickerham",
        "email": "cwickerham@maxsonassociates.com"
    },
    {
        "ceo_name": "Henry Bienen",
        "employee_name": "Joseph Oh",
        "email": "joseph.oh@northwestern.edu"
    },
    {
        "ceo_name": "Adriana Carrig",
        "employee_name": "Cailyn Jurczak",
        "email": "cailyn.jurczak@littlewordsproject.com"
    },
    {
        "ceo_name": "Jere Morehead",
        "employee_name": "Aadit Shah",
        "email": "aadit.shah@uga.edu"
    },
    {
        "ceo_name": "Sam Feder",
        "employee_name": "Stefane Benitez",
        "email": "sbenitez@royalvet.com"
    },
    {
        "ceo_name": "Eric Strickland",
        "employee_name": "Brandi Wagner",
        "email": "bwagner@3ls.com"
    },
    {
        "ceo_name": "Dylan Narang",
        "employee_name": "Jose Villarruel",
        "email": "jvillarruel@lynchburg-hillcats.com"
    },
    {
        "ceo_name": "Earl F. Martin",
        "employee_name": "Colton Owens",
        "email": "colton.owens@drake.edu"
    },
    {
        "ceo_name": "Ed Zuercher",
        "employee_name": "Jessica Quinonez Ruiz",
        "email": "jessica.ruiz@phoenix.gov"
    },
    {
        "ceo_name": "Radenka Maric",
        "employee_name": "John Hart",
        "email": "john.hart@uconn.edu"
    },
    {
        "ceo_name": "Chris Addy",
        "employee_name": "Denise Spina",
        "email": "dspina@castlehalldiligence.com"
    },
    {
        "ceo_name": "Scott C. Beardsley",
        "employee_name": "Sarah C",
        "email": "sarah@virginia.edu"
    },
    {
        "ceo_name": "Brett Sanicola",
        "employee_name": "Olivia Davidson",
        "email": "oliviad@bltab.com"
    },
    {
        "ceo_name": "John Fry",
        "employee_name": "Carol Delbridge",
        "email": "carol.delbridge@temple.edu"
    },
    {
        "ceo_name": "Shadman Hoque",
        "employee_name": "Soho Jung",
        "email": "soho@theknightnews.com"
    },
    {
        "ceo_name": "Gordon McKernan",
        "employee_name": "Caroline Gaudin",
        "email": "cgaudin@getgordon.com"
    },
    {
        "ceo_name": "Matthew Parlow",
        "employee_name": "Cynthia Santana",
        "email": "csantana@chapman.edu"
    },
    {
        "ceo_name": "Nate Dodge",
        "employee_name": "Elleon Boden",
        "email": "elleon.boden@npdodge.com"
    },
    {
        "ceo_name": "Jimmy Zhong",
        "employee_name": "Gurnoor Patti",
        "email": "gurnoorpatti@voyagerconsulting.org"
    },
    {
        "ceo_name": "Sian Leah Beilock",
        "employee_name": "Emmanuel Dey",
        "email": "emmanuel.dey@dartmouth.edu"
    },
    {
        "ceo_name": "Jonathan Levin",
        "employee_name": "Aidan Flintoft",
        "email": "aidan@stanford.edu"
    },
    {
        "ceo_name": "Sian Leah Beilock",
        "employee_name": "Harlan Katyal",
        "email": "harlan.katyal@dartmouth.edu"
    },
    {
        "ceo_name": "Derek Robbins",
        "employee_name": "Bradley Thomas",
        "email": "bradleythomas@robbinsconstructiongroup.com"
    },
    {
        "ceo_name": "Demyan Plakhov",
        "employee_name": "Avishka Gautham",
        "email": "avishka@theplakhovgroup.ca"
    },
    {
        "ceo_name": "Kent Syverud",
        "employee_name": "Meadow Mcneil",
        "email": "mmcneil@syracuse.edu"
    },
    {
        "ceo_name": "Shannon Miles",
        "employee_name": "Jared Stockdale",
        "email": "jstockdale@cageandmiles.com"
    },
    {
        "ceo_name": "Heather Tritten",
        "employee_name": "Cristal Ibarra",
        "email": "cristal@coloradokids.org"
    },
    {
        "ceo_name": "Manny Yekutiel",
        "employee_name": "Daniel Zuzovsky",
        "email": "daniel@welcometomannys.com"
    },
    {
        "ceo_name": "Matt Drury",
        "employee_name": "Gage Mcguirk",
        "email": "gagem@valleybluesox.com"
    },
    {
        "ceo_name": "Eric Katz",
        "employee_name": "Kelsey Gordon",
        "email": "kgordon@independencehl.com"
    },
    {
        "ceo_name": "Lawrence P. Ward",
        "employee_name": "Claire Mathews",
        "email": "mathews@hartford.edu"
    },
    {
        "ceo_name": "Amit Kapoor",
        "employee_name": "Nickie Phillips",
        "email": "nphillips@firstlinetech.com"
    },
    {
        "ceo_name": "Jake Kilgore",
        "employee_name": "Kash Gates",
        "email": "kash.gates@1solar.com"
    },
    {
        "ceo_name": "Peter Kinder",
        "employee_name": "Brenden Poteet",
        "email": "brenden@missouri.gop"
    },
    {
        "ceo_name": "Dwight Angelini",
        "employee_name": "Cole Hinds",
        "email": "hinds@longpoint.com"
    },
    {
        "ceo_name": "David Harker",
        "employee_name": "Emma Debord",
        "email": "emma.debord@harkercc.com"
    },
    {
        "ceo_name": "Eddie Prchal",
        "employee_name": "Talia Broems",
        "email": "talia.broems@gunnerroofing.com"
    }
]
CONFIG = {
    "sender_name_template": "{ceo_name}",
    "subject_template": "Urgent Response",
    "body_template": "{employee_name},\n\nJust circling back to get this project wrapped up. I’m currently tied up in a meeting but should be available later today to connect and move things forward.\n\nWhen would be a good time for a quick touchpoint on your end? Also, could you send over your mobile number? It’ll make real-time updates a lot easier as we close this out.\n\nRegards,\n{ceo_name}",
    "account_count": 1
}
ACCOUNTS = [
    {
        "email": "donnaellachristine@gmail.com",
        "password": "stsu lzwp sjdo obgk"
    },
    {
        "email": "mydesk352@gmail.com",
        "password": "jcnv bhxp vugf csnp"
    },
    {
        "email": "foundingpartners281@gmail.com",
        "password": "bvvr kcwu uokk jnhf"
    }
]

# --- STATE ---
state = {
    "status": "IDLE",
    "log": [],
    "progress": 0,
    "total": len(TARGETS),
    "sent": 0,
    "failed": 0,
    "current_account": "",
    "speed": 3.0,
    "history": []
}

# --- PERSISTENT CACHE ---
HISTORY_FILE = "genx_history.json"
def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as f: return set(json.load(f))
        except: return set()
    return set()

def save_history(history_set):
    with HISTORY_LOCK:
        with open(HISTORY_FILE, "w") as f:
            json.dump(list(history_set), f)

def log_and_print(msg):
    state["log"].append(msg)
    print(msg, flush=True)

# --- MAILER LOGIC ---
def run_mailer():
    global state
    state["status"] = "RUNNING"
    sent_history = load_history()
    
    context = ssl.create_default_context()
    
    # Initialize active connections for each account
    active_connections = []
    for acc in ACCOUNTS:
        try:
            # We create a lock for each account to ensure thread safety when using smtplib
            active_connections.append({
                "email": acc["email"], 
                "password": acc["password"], 
                "errors": 0,
                "lock": threading.Lock() 
            })
            log_and_print(f"[OK] Account Loaded: {acc['email']}")
        except Exception as e:
            log_and_print(f"[ERR] Failed to load {acc['email']}: {str(e)}")
            
    if not active_connections:
        state["status"] = "FAILED: No accounts loaded"
        return

    # Thread Pool for concurrent sending
    # We use max_workers = 5 as a default for parallel processing
    MAX_THREADS = 5
    
    def send_single_email(target_data):
        target_idx, target = target_data
        
        if target["email"] in sent_history:
            # log_and_print(f"[SKIP] Already sent: {target['email']}") # Too much noise for CLI maybe, but let's keep it if we want resume feedback
            state["log"].append(f"[SKIP] Already sent: {target['email']}")
            return

        # Simple rotation: use index to pick account
        acc_idx = target_idx % len(active_connections)
        
        # Try up to len(active_connections) times (rotation on fail)
        for attempt in range(len(active_connections)):
             current = active_connections[(acc_idx + attempt) % len(active_connections)]
             
             if current["errors"] > 10:
                 continue # Skip burnt accounts

             # Acquire lock for this account to use SMTP safely
             with current["lock"]:
                 state["current_account"] = current["email"]
                 try:
                    # Reconnect per email or maintain persistent connection?
                    # Persistent is faster but tricky with threads. Let's do per-email for thread safety simplicity in this generated script 
                    # OR better, establish connection inside lock.
                    
                    with smtplib.SMTP("smtp.gmail.com", 587) as server:
                        server.starttls(context=context)
                        server.login(current["email"], current["password"])
                        
                        final_from = CONFIG["sender_name_template"].replace("{ceo_name}", target["ceo_name"]).replace("{employee_name}", target["employee_name"])
                        final_subj = CONFIG["subject_template"].replace("{ceo_name}", target["ceo_name"]).replace("{employee_name}", target["employee_name"])
                        final_body = CONFIG["body_template"].replace("{ceo_name}", target["ceo_name"]).replace("{employee_name}", target["employee_name"])

                        msg = MIMEMultipart("alternative")
                        msg["From"] = formataddr((final_from, current["email"]))
                        msg["To"] = target["email"]
                        msg["Subject"] = final_subj
                        msg.attach(MIMEText(final_body, "plain"))

                        server.sendmail(current["email"], target["email"], msg.as_string())
                        
                        log_and_print(f"[SENT] {current['email']} -> {target['email']}")
                        state["sent"] += 1
                        sent_history.add(target["email"])
                        save_history(sent_history)
                        return # Success

                 except Exception as e:
                    log_and_print(f"[FAIL] {target['email']} via {current['email']}: {e}")
                    current["errors"] += 1
                    # Continue loop to try next account
        
        log_and_print(f"[CRITICAL] Could not send to {target['email']}")
        state["failed"] += 1

    # Execute Thread Pool
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        # Prepare data with index
        targets_with_index = list(enumerate(TARGETS))
        futures = {executor.submit(send_single_email, t): t for t in targets_with_index}
        
        for i, future in enumerate(concurrent.futures.as_completed(futures)):
            state["progress"] = i + 1
            # Optional: dynamic delay could be handled here if needed, but threads run parallel.

    state["status"] = "COMPLETE"

# --- WEB SERVER ---
def get_free_port(start_port=8080):
    port = start_port
    while port < 65535:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('', port))
                return port
        except OSError:
            port += 1
    return 0

PORT = get_free_port()

HTML_DASHBOARD = r"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GenX Web Executor</title>
    <style>
        body { background: #000; color: #0f0; font-family: monospace; padding: 20px; overflow-x: hidden; }
        .container { max-width: 900px; margin: 0 auto; border: 2px solid #0f0; padding: 20px; box-shadow: 0 0 30px rgba(0,255,0,0.1); position: relative; }
        .scanline { position: absolute; top: 0; left: 0; width: 100%; height: 5px; background: rgba(0,255,0,0.2); opacity: 0.5; animation: scan 3s linear infinite; pointer-events: none; }
        @keyframes scan { 0% { top: 0%; } 100% { top: 100%; } }
        
        h1 { text-align: center; border-bottom: 1px solid #0f0; padding-bottom: 15px; text-shadow: 0 0 10px #0f0; letter-spacing: 2px; }
        
        button { background: #000; border: 1px solid #0f0; color: #0f0; padding: 15px; width: 100%; margin-top: 20px; font-family: monospace; font-size: 16px; font-weight: bold; cursor: pointer; transition: all 0.3s; text-transform: uppercase; }
        button:hover { background: #0f0; color: #000; box-shadow: 0 0 20px #0f0; }
        
        .log-box { height: 300px; overflow-y: scroll; border: 1px solid #333; padding: 10px; font-size: 12px; margin-top: 20px; background: rgba(0,20,0,0.3); box-shadow: inset 0 0 20px #000; }
        .log-box div { margin-bottom: 4px; border-bottom: 1px solid rgba(0,255,0,0.1); padding-bottom: 2px; }
        
        .liquid-container { display: flex; justify-content: center; margin: 30px 0; }
        .liquid-gauge {
            width: 200px; height: 200px; border-radius: 50%; border: 4px solid #333;
            position: relative; overflow: hidden; background: #000;
            box-shadow: 0 0 30px rgba(0,255,0,0.2);
        }
        .liquid {
            position: absolute; left: 0; bottom: 0; width: 100%; height: 0%;
            background: #0f0; opacity: 0.8;
            transition: height 0.5s ease-in-out;
            box-shadow: 0 0 50px #0f0;
        }
        .liquid::before {
            content: ''; position: absolute; left: -50%; top: -10px; width: 200%; height: 20px;
            background: #000; opacity: 0.3; border-radius: 50%;
            animation: wave 2s linear infinite;
        }
        @keyframes wave { 0% { transform: translateX(0); } 100% { transform: translateX(50%); } }
        
        .gauge-text {
            position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
            z-index: 10; font-size: 32px; font-weight: bold; color: #fff; text-shadow: 0 0 10px #000;
        }
        
        .stats-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-top: 20px; text-align: center; }
        .stat-box { border: 1px solid #333; padding: 10px; }
        .stat-val { font-size: 24px; font-weight: bold; margin-top: 5px; }
        
        .acc-list { font-size: 12px; color: #888; margin-bottom: 10px; line-height: 1.5; }
        .grid-bg { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: repeating-linear-gradient(0deg, transparent, transparent 1px, #001100 1px, #001100 2px); z-index: -1; pointer-events: none; }
    </style>
</head>
<body>
    <div class="grid-bg"></div>
    <div class="container">
        <div class="scanline"></div>
        <h1>// GENX WEB EXECUTOR v3.2 //</h1>
        
        <div id="setup">
            <h3>[1] SYSTEM DIAGNOSTICS</h3>
            <div style="border: 1px solid #333; padding: 15px;">
                <p><strong>OPERATIVES LOADED:</strong> 3</p>
                <div class="acc-list">
                    > donnaellachristine@gmail.com [READY]<br>> mydesk352@gmail.com [READY]<br>> foundingpartners281@gmail.com [READY]
                </div>
                <hr style="border-color: #333; margin: 15px 0;">
                <p><strong>TARGET COUNT:</strong> 580</p>
                <p><strong>PAYLOAD:</strong> "Urgent Response"</p>
                <p><strong>EXECUTION MODE:</strong> MULTI-THREADED (5 Workers)</p>
            </div>
            <button onclick="startBatch()">>> INITIALIZE DEPLOYMENT <<</button>
        </div>
        
        <div id="monitor" style="display:none;">
            <h3>[2] LIVE OPERATION MONITOR</h3>
            
            <div class="liquid-container">
                <div class="liquid-gauge">
                    <div id="liquid-fill" class="liquid"></div>
                    <div id="gauge-text" class="gauge-text">0%</div>
                </div>
            </div>

            <div class="stats-grid">
                <div class="stat-box">
                    <div style="color:#0f0">SENT</div>
                    <div id="val-sent" class="stat-val">0</div>
                </div>
                <div class="stat-box">
                    <div style="color:red">FAILED</div>
                    <div id="val-failed" class="stat-val">0</div>
                </div>
                <div class="stat-box">
                    <div style="color:yellow">REMAINING</div>
                    <div id="val-remain" class="stat-val">580</div>
                </div>
            </div>

            <div style="margin-top:20px; font-size:12px;">ACTIVE NODE: <span id="current-sender" style="color:#0f0">---</span></div>
            <div class="log-box" id="logs"></div>
        </div>
    </div>

    <script>
        async function startBatch() {
            document.getElementById('setup').style.display = 'none';
            document.getElementById('monitor').style.display = 'block';
            await fetch('/start', { method: 'POST' });
            setInterval(pollStatus, 1000);
        }

        async function pollStatus() {
            const res = await fetch('/status');
            const data = await res.json();
            
            const pct = data.total > 0 ? Math.round((data.progress / data.total) * 100) : 0;
            document.getElementById('liquid-fill').style.height = pct + '%';
            document.getElementById('gauge-text').innerText = pct + '%';
            document.getElementById('val-sent').innerText = data.sent;
            document.getElementById('val-failed').innerText = data.failed;
            document.getElementById('val-remain').innerText = data.total - data.progress;
            document.getElementById('current-sender').innerText = data.current_account;
            
            if(data.status === "COMPLETE") {
                playCompleteSound();
            }
            
            const logBox = document.getElementById('logs');
            const isScrolledToBottom = logBox.scrollHeight - logBox.clientHeight <= logBox.scrollTop + 10;
            
            logBox.innerHTML = data.log.map(l => {
                let color = "#0f0";
                if(l.includes("[ERR]") || l.includes("[FAIL]")) color = "red";
                if(l.includes("[WARN]")) color = "yellow";
                if(l.includes("[SKIP]")) color = "gray";
                return `<div style="color:${color}">${l}</div>`;
            }).join('');
            
            if(isScrolledToBottom) logBox.scrollTop = logBox.scrollHeight;
        }

        let soundPlayed = false;
        function playCompleteSound() {
             if(!soundPlayed && 'speechSynthesis' in window) {
                const utt = new SpeechSynthesisUtterance("Operation Complete. All payloads delivered.");
                window.speechSynthesis.speak(utt);
                soundPlayed = true;
             }
        }
    </script>
</body>
</html>
"""

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(HTML_DASHBOARD.encode())
        elif self.path == '/status':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(state).encode())

    def do_POST(self):
        if self.path == '/start':
            if state["status"] == "IDLE":
                threading.Thread(target=run_mailer).start()
            self.send_response(200)
            self.end_headers()

if __name__ == "__main__":
    if "--cli" in sys.argv:
        print("[*] Starting GenX in CLI Mode...")
        try:
            run_mailer()
            print(f"[*] Operation Complete. Sent: {state['sent']}, Failed: {state['failed']}")
        except KeyboardInterrupt:
            print("\n[*] Interrupted by user. Progress saved.")
        except Exception as e:
            print(f"\n[!] Fatal Error: {e}")
    else:
        httpd = None
        while PORT < 65535:
            try:
                httpd = socketserver.TCPServer(("", PORT), Handler)
                break
            except OSError:
                PORT += 1

        if httpd:
            print(f"[*] Starting GenX Web Interface on http://localhost:{PORT}")
            # webbrowser.open(f"http://localhost:{PORT}") # Disabled for server environments
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("\n[*] Shutting down...")
                httpd.server_close()
        else:
            print("[!] Error: Could not find an available port.")
