import main_scraper
import secondary_scraper

from main_scraper import Stats_Scraper
# from secondary_scraper import secondSiteScraper


if __name__ == '__main__':

    data_grabber = Stats_Scraper()
    
    goals = data_grabber.stat_scrape("https://www.premierleague.com/stats/top/players/goals")
    assists = data_grabber.stat_scrape("https://www.premierleague.com/stats/top/players/goal_assist")
    appearances = data_grabber.stat_scrape("https://www.premierleague.com/stats/top/players/appearances")
    minutes_played = data_grabber.stat_scrape("https://www.premierleague.com/stats/top/players/mins_played")
    shots_taken = data_grabber.stat_scrape("https://www.premierleague.com/stats/top/players/total_scoring_att")
    shots_on_target = data_grabber.stat_scrape("https://www.premierleague.com/stats/top/players/ontarget_scoring_att")
    passes = data_grabber.stat_scrape("https://www.premierleague.com/stats/top/players/total_pass")
    crosses = data_grabber.stat_scrape("https://www.premierleague.com/stats/top/players/total_cross")
    through_balls = data_grabber.stat_scrape("https://www.premierleague.com/stats/top/players/total_through_ball")
    interceptions = data_grabber.stat_scrape("https://www.premierleague.com/stats/top/players/interception")
    tackles = data_grabber.stat_scrape("https://www.premierleague.com/stats/top/players/total_tackle")
    clearances = data_grabber.stat_scrape("https://www.premierleague.com/stats/top/players/total_clearance")
    blocks = data_grabber.stat_scrape("https://www.premierleague.com/stats/top/players/outfielder_block")
    aerial_battles = data_grabber.stat_scrape("https://www.premierleague.com/stats/top/players/aerial_won")
    
    data_grabber.stopDriver()

    # data_grabber2 = secondSiteScraper()

    # data_grabber2.getPlayerStats()

    # data_grabber2.stopDriver()