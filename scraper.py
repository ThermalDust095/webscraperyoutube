import youtube_dl
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager  # Automatically manage ChromeDriver
from selenium.webdriver.common.keys import Keys
import time
import yt_dlp
import time 


def get_playlist_info(playlist_url):
    ydl_opts = {
        'quiet': True,
        'extract_flat': 'in_playlist',  # To extract only the video info without downloading
        'skip_download': True
    }
    
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        playlist_info = ydl.extract_info(playlist_url, download=False)

    videos = []
    if 'entries' in playlist_info:
        for entry in playlist_info['entries']:
            video_info = {
                'title': entry.get('title'),
                'url': f"https://www.youtube.com/watch?v={entry.get('id')}",
                'duration': entry.get('duration')
            }
            videos.append(video_info)
    
    return videos


def get_playlist_details(playlist_url):
    # Define the options for yt-dlp
    ydl_opts = {
        'quiet': True,  # Suppresses output
        'extract_flat': True,  # Only extract information without downloading
        'force_generic_extractor': True,
    }

    # Create a yt-dlp object
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # Extract playlist information
        info_dict = ydl.extract_info(playlist_url, download=False)
        playlist_name = info_dict.get('title', 'Unknown Playlist')
        playlist_description = info_dict.get('description', 'No description available.')
        total_duration = sum(entry.get('duration', 0) for entry in info_dict.get('entries', []))

        print(f'scraping  {playlist_name}....')

    # Convert total duration from seconds to hours, minutes, and seconds
    hours, remainder = divmod(total_duration, 3600)
    minutes, seconds = divmod(remainder, 60)
    duration_str = f"{hours} hours, {minutes} minutes, and {seconds} seconds" if hours > 0 else f"{minutes} minutes and {seconds} seconds"

    return playlist_name, duration_str

def get_search_url(query):
    query = query.replace(' ', '+')
    return f"https://www.youtube.com/results?search_query={query}+playlist&sp=EgIQAw%253D%253D"

def get_playlist_link(search_url):
    # Setup Selenium WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(search_url)
    
    # Allow time for the page to load
    time.sleep(3)
    
    try:
        # Find the first playlist link
        playlists = driver.find_elements(By.XPATH, '//a[contains(@href, "list=")]')
        if playlists:
            playlist_url = playlists[0].get_attribute('href')
        else:
            playlist_url = None
    finally:
        driver.quit()
    
    return playlist_url

def main(query):
    search_url = get_search_url(query)
    playlist_url = get_playlist_link(search_url)
    
    if playlist_url:
        print(f"Playlist URL for '{query}': {playlist_url}")
    else:
        print(f"No playlist found for '{query}'")

INFROMATION_TO_SAVE_INTO_CSV = []

def scrape_playlist(query ,sector ,INFROMATION_TO_SAVE_INTO_CSV):
    search_url = get_search_url(query)
    playlist_url = get_playlist_link(search_url)
    # NOTE THAT playlist_url as &list parameter in the URL 
    name , duration = get_playlist_details(playlist_url)
    
    videos_info = get_playlist_info(playlist_url)
    
    ## Start scrapping
    total_duration = 0
    num_videos = len(videos_info)
    
    for n, video in enumerate(videos_info):
        vid_title = str(video['title'])
        vid_url = str(video['url'])
        vid_duration = int(video['duration'])
        total_duration += vid_duration
        
        if n == 0:
            #append at end
            INFROMATION_TO_SAVE_INTO_CSV.append([sector, name, f'{total_duration//3600}hrs {total_duration%3600}min', vid_title, vid_url]) 
        else:
            INFROMATION_TO_SAVE_INTO_CSV.append([ sector, name,'', vid_title, vid_url])

if __name__ == "__main__":
    
    sectors = {
    "Performing Arts": [
        "Acting", "Dance", "Directing", "Playwriting", "Theatre History",
        "Stagecraft", "Musical Theatre", "Voice and Speech", "Movement for Actors",
        "Theatre Production", "Theatre Design", "Costume Design", "Lighting Design",
        "Sound Design", "Dramaturgy", "Theatre Management", "Theatre Criticism",
        "Theatre for Social Change", "Theatre Education", "Film Acting"
    ],
    "Film and Media Studies": [
        "Film History", "Film Theory", "Screenwriting", "Film Production", "Film Editing",
        "Cinematography", "Sound Design", "Documentary Filmmaking", "Film Criticism",
        "Film Directing", "Media Studies", "Digital Media Production", "Animation",
        "Visual Effects", "Media Ethics", "Television Studies", "Media Law",
        "Media Management", "Media Psychology", "Film and Society"
    ],
    "Journalism": [
        "News Writing", "Reporting", "Media Law", "Broadcast Journalism", "Investigative Journalism",
        "Photojournalism", "Digital Journalism", "Feature Writing", "Media Ethics", "Data Journalism",
        "Editing", "Journalism History", "International Journalism", "Sports Journalism",
        "Business Journalism", "Political Reporting", "Science Journalism", "Environmental Reporting",
        "Journalism and Social Media", "Multimedia Storytelling"
    ],
    "Photography": [
        "Photography Basics", "Digital Photography", "Portrait Photography", "Landscape Photography",
        "Studio Photography", "Photojournalism", "Black and White Photography", "Photography Lighting",
        "Photography Composition", "Fine Art Photography", "Commercial Photography", "Travel Photography",
        "Documentary Photography", "Fashion Photography", "Sports Photography", "Event Photography",
        "Photography Post-Processing", "Photography Business", "Wildlife Photography", "Photography Critique"
    ],
    "Culinary Arts": [
        "Culinary Fundamentals", "Baking and Pastry", "International Cuisine", "Food Safety and Sanitation",
        "Culinary Techniques", "Nutrition", "Culinary Management", "Food and Beverage Pairing",
        "Culinary Science", "Garde Manger", "Advanced Pastry", "Culinary Innovation", "Food Styling",
        "Restaurant Operations", "Culinary Marketing", "Farm-to-Table", "Sustainable Culinary Practices",
        "Culinary Arts History", "Culinary Arts Education", "Culinary Arts Portfolio"
    ],
    "Hospitality Management": [
        "Hospitality Operations", "Hotel Management", "Food and Beverage Management", "Event Planning",
        "Tourism Management", "Hospitality Marketing", "Hospitality Law", "Customer Service",
        "Revenue Management", "Hospitality Accounting", "Resort Management", "Hospitality Information Systems",
        "Sustainable Tourism", "Hospitality Leadership", "Hospitality Sales", "Travel and Tourism",
        "Hospitality Human Resources", "Lodging Management", "Hospitality Entrepreneurship", "Hospitality Trends"
    ],
    "Travel and Tourism": [
        "Tourism Principles", "Travel Planning", "Destination Management", "Tourism Marketing",
        "Eco-Tourism", "Sustainable Tourism", "Cultural Tourism", "Adventure Tourism",
        "Cruise Management", "Airline Management", "Tour Operations", "Hospitality and Tourism Law",
        "Tourism Economics", "Travel Agency Operations", "Tourism Policy", "Event Tourism",
        "Heritage Tourism", "Tourism Technology", "Health and Wellness Tourism", "Tourism Research"
    ],
    "Sports Management": [
        "Sports Marketing", "Sports Law", "Sports Finance", "Event Management", "Sports Psychology",
        "Sports Ethics", "Sports Facility Management", "Sports Media", "Sports Analytics", "Sports Sponsorship",
        "Athlete Management", "Sports Economics", "Sports Governance", "Sports Medicine", "Youth Sports Management",
        "Esports Management", "Sports Tourism", "Community Sports", "Sports Public Relations", "Sports Leadership"
    ],
    "Physical Education": [
        "Exercise Physiology", "Kinesiology", "Sports Coaching", "Physical Education Curriculum",
        "Sports Psychology", "Motor Learning", "Adapted Physical Education", "Health Education",
        "Sports Nutrition", "Biomechanics", "Physical Fitness Assessment", "Outdoor Education",
        "Sports Pedagogy", "Team Sports", "Individual Sports", "Physical Activity and Health",
        "Physical Education Research", "Sports Administration", "Dance Education", "Physical Education Technology"
    ],
    "Linguistics": [
        "Phonetics", "Phonology", "Morphology", "Syntax", "Semantics", "Pragmatics", "Sociolinguistics",
        "Psycholinguistics", "Historical Linguistics", "Computational Linguistics", "Language Acquisition",
        "Language Documentation", "Forensic Linguistics", "Applied Linguistics", "Discourse Analysis",
        "Neurolinguistics", "Language and Culture", "Corpus Linguistics", "Bilingualism", "Translation Studies"
    ],
    "Psychology": [
        "Clinical Psychology", "Developmental Psychology", "Cognitive Psychology", "Social Psychology",
        "Personality Psychology", "Industrial-Organizational Psychology", "Educational Psychology",
        "Health Psychology", "Forensic Psychology", "Neuropsychology", "Child Psychology", "Abnormal Psychology",
        "Counseling Psychology", "Behavioral Psychology", "Experimental Psychology", "Psychometrics",
        "Sport Psychology", "Positive Psychology", "Environmental Psychology", "Cultural Psychology"
    ],
    "Sociology": [
        "Classical Sociological Theory", "Contemporary Sociological Theory", "Social Stratification",
        "Gender Studies", "Race and Ethnicity", "Urban Sociology", "Rural Sociology", "Sociology of Education",
        "Sociology of Family", "Medical Sociology", "Criminology", "Sociology of Religion", "Political Sociology",
        "Sociology of Law", "Sociology of Work", "Sociology of Aging", "Sociology of Science",
        "Environmental Sociology", "Cultural Sociology", "Economic Sociology"
    ],
    "Anthropology": [
        "Cultural Anthropology", "Biological Anthropology", "Archaeology", "Linguistic Anthropology",
        "Medical Anthropology", "Forensic Anthropology", "Environmental Anthropology", "Urban Anthropology",
        "Visual Anthropology", "Economic Anthropology", "Ethnography", "Applied Anthropology",
        "Anthropology of Religion", "Political Anthropology", "Anthropology of Art", "Kinship and Family",
        "Anthropological Theory", "Indigenous Studies", "Anthropology of Development", "Globalization and Culture"
    ],
    "Political Science": [
        "Political Theory", "Comparative Politics", "International Relations", "Public Policy",
        "Political Economy", "Political Sociology", "Political Psychology", "Public Administration",
        "Political Methodology", "American Politics", "European Politics", "Asian Politics", "African Politics",
        "Latin American Politics", "Middle Eastern Politics", "Political Communication", "Political Philosophy",
        "Political Campaigns", "Environmental Politics", "Human Rights"
    ],
    "International Relations": [
        "International Relations Theory", "International Security", "Global Governance", "Foreign Policy Analysis",
        "International Organizations", "International Political Economy", "Peace and Conflict Studies",
        "Diplomatic Studies", "International Law", "Humanitarian Intervention", "Regional Studies",
        "International Development", "Globalization", "International Trade", "Transnational Issues",
        "International Negotiation", "Migration and Refugee Studies", "Global Health Politics",
        "Cybersecurity in International Relations", "Environmental Diplomacy"
    ]
}    

    for s in sectors.keys():
        for el in sectors[s]:
            try:
                scrape_playlist(el, s,INFROMATION_TO_SAVE_INTO_CSV)
                print("scraped..")
            except:
                print(f"couldnt scrape sector:{s},, {el} ")
                pass

    data= pd.DataFrame(INFROMATION_TO_SAVE_INTO_CSV)
    data.columns=['Sector','CourseName', 'Duration', 'TopicName', 'URL']
    data.to_csv("./scraped_data5.csv")