# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod


class Player:
    BATTING = "打撃成績"
    PITCHING = "投手成績"
    BATTER = "batter"
    PITCHER = "pitcher"
    AT_LEAST_GAMES_FOR_BATTER = 1000
    AT_LEAST_GAMES_FOR_PITCHER = 100
    OHTANI = "大谷　翔平"
    CATEGORY_FOR_OHTANI = "batter/pitcher"

    def create_player(self, response, name):
        stat = []
        if name == self.OHTANI:
            category = self.CATEGORY_FOR_OHTANI
            target = self.create_ohtani()
        else:
            category = self.get_category(response)
            if category == self.BATTER:
                target = self.create_batter()
            elif category == self.PITCHER:
                target = self.create_pitcher()
            else:
                raise Exception("野手、投手以外のデータが対象となっています。")
            if target.is_less_than_expectation(response):
                return [None, None]
        stat = target.begin_setting_stat(response, stat)
        return [category, stat]

    def get_category(self, response):
        category = response.xpath("//table[@class='ind1'][1]/caption/text()").extract_first()
        if category == self.BATTING:
            return self.BATTER
        elif category == self.PITCHING:
            return self.PITCHER
        else:
            raise Exception("打撃成績、投手成績以外のデータが対象となっています。")

    def create_batter(self):
        return Batter()

    def create_pitcher(self):
        return Pitcher()

    def create_ohtani(self):
        return Ohtani()

    @abstractmethod
    def is_less_than_expectation(self, response):
        pass

    @abstractmethod
    def begin_setting_stat(self, response, stat):
        pass

    @abstractmethod
    def set_stat(self, job, stat):
        pass

    def get_rid_of_range(self, job):
        if job.xpath("td[1]/text()").extract_first() in ["年", "国内通算", "MLB通算"]:
            return True
        return False


class Batter(Player):
    def is_less_than_expectation(self, response):
        total_games = int(response.xpath(
                          "//table[@class='ind1'][1]/tr[@class='title2']/td[2]/text()")
                          .extract_first())
        if total_games < Player.AT_LEAST_GAMES_FOR_BATTER:
            return True
        return False

    def begin_setting_stat(self, response, stat):
        jobs = response.xpath("//table[@class='ind1'][1]/tr")
        for job in jobs:
            if self.get_rid_of_range(job):
                continue
            stat = self.set_stat(job, stat)
        return stat

    def set_stat(self, job, stat):
        data = {}
        data["year"] = job.xpath("td[1]/text()").extract_first()
        data["team"] = job.xpath("td[@class='tm']/text()").extract_first()
        data["number"] = job.xpath("td[@class='seban']/text()").extract_first()
        data["age"] = job.xpath("td[36]/text()").extract_first()
        data["games_played"] = (job.xpath("td[5]/text()").extract_first()
                                if job.xpath("td[5]/text()").extract_first() is not None
                                else job.xpath("td[5]/b/text()").extract_first())
        data["plate_appearances"] = (job.xpath("td[6]/text()").extract_first()
                                     if job.xpath("td[6]/text()").extract_first() is not None
                                     else job.xpath("td[6]/b/text()").extract_first())
        data["at_bats"] = (job.xpath("td[7]/text()").extract_first()
                           if job.xpath("td[7]/text()").extract_first() is not None
                           else job.xpath("td[7]/b/text()").extract_first())
        data["runs_scored"] = (job.xpath("td[8]/text()").extract_first()
                               if job.xpath("td[8]/text()").extract_first() is not None
                               else job.xpath("td[8]/b/text()").extract_first())
        data["hits"] = (job.xpath("td[9]/text()").extract_first()
                        if job.xpath("td[9]/text()").extract_first() is not None
                        else job.xpath("td[9]/b/text()").extract_first())
        data["double_hits"] = (job.xpath("td[10]/text()").extract_first()
                               if job.xpath("td[10]/text()").extract_first() is not None
                               else job.xpath("td[10]/b/text()").extract_first())
        data["triples_hits"] = (job.xpath("td[11]/text()").extract_first()
                                if job.xpath("td[11]/text()").extract_first() is not None
                                else job.xpath("td[11]/b/text()").extract_first())
        data["home_runs"] = (job.xpath("td[@class='batter'][1]/text()").extract_first()
                             if job.xpath("td[@class='batter'][1]/text()").extract_first() is not None
                             else job.xpath("td[@class='batter'][1]/b/text()").extract_first())
        data["runs_battled_in"] = (job.xpath("td[@class='batter'][2]/text()").extract_first()
                                   if job.xpath("td[@class='batter'][2]/text()").extract_first() is not None
                                   else job.xpath("td[@class='batter'][2]/b/text()").extract_first())
        data["stolen_bases"] = (job.xpath("td[15]/text()").extract_first()
                                if job.xpath("td[15]/text()").extract_first() is not None
                                else job.xpath("td[15]/b/text()").extract_first())
        data["caught_stealing"] = (job.xpath("td[16]/text()").extract_first()
                                   if job.xpath("td[16]/text()").extract_first() is not None
                                   else job.xpath("td[16]/b/text()").extract_first())
        data["sacrifice_hits"] = (job.xpath("td[17]/text()").extract_first()
                                  if job.xpath("td[17]/text()").extract_first() is not None
                                  else job.xpath("td[17]/b/text()").extract_first())
        data["sacrifice_flies"] = (job.xpath("td[18]/text()").extract_first()
                                   if job.xpath("td[18]/text()").extract_first() is not None
                                   else job.xpath("td[18]/b/text()").extract_first())
        data["walks"] = (job.xpath("td[19]/text()").extract_first()
                         if job.xpath("td[19]/text()").extract_first() is not None
                         else job.xpath("td[19]/b/text()").extract_first())
        data["intentional_bases_on_balls"] = (job.xpath("td[20]/text()").extract_first()
                                              if job.xpath("td[20]/text()").extract_first() is not None
                                              else job.xpath("td[20]/b/text()").extract_first())
        data["hit_by_pitch"] = (job.xpath("td[21]/text()").extract_first()
                                if job.xpath("td[21]/text()").extract_first() is not None
                                else job.xpath("td[21]/b/text()").extract_first())
        data["strikeouts"] = (job.xpath("td[22]/text()").extract_first()
                              if job.xpath("td[22]/text()").extract_first() is not None
                              else job.xpath("td[22]/b/text()").extract_first())
        data["double_play_grounded_into"] = (job.xpath("td[23]/text()").extract_first()
                                             if job.xpath("td[23]/text()").extract_first() is not None
                                             else job.xpath("td[23]/b/text()").extract_first())
        data["batting_average"] = (job.xpath("td[@class='batter'][3]/text()").extract_first()
                                   if job.xpath("td[@class='batter'][3]/text()").extract_first() is not None
                                   else job.xpath("td[@class='batter'][3]/b/text()").extract_first())
        data["obp"] = (job.xpath("td[29]/text()").extract_first()
                       if job.xpath("td[29]/text()").extract_first() is not None
                       else job.xpath("td[29]/b/text()").extract_first())
        data["slg"] = (job.xpath("td[30]/text()").extract_first()
                       if job.xpath("td[30]/text()").extract_first() is not None
                       else job.xpath("td[30]/b/text()").extract_first())
        data["ops"] = (job.xpath("td[31]/text()").extract_first()
                       if job.xpath("td[31]/text()").extract_first() is not None
                       else job.xpath("td[31]/b/text()").extract_first())
        data["positions"] = (job.xpath("td[32]/text()").extract_first()
                             if job.xpath("td[32]/text()").extract_first() is not None
                             else job.xpath("td[32]/b/text()").extract_first())
        stat.append(data.copy())
        return stat


class Pitcher(Player):
    def is_less_than_expectation(self, response):
        total_games = int(response.xpath(
                          "//table[@class='ind1'][1]/tr[@class='title2']/td[2]/text()")
                          .extract_first())
        if total_games < Player.AT_LEAST_GAMES_FOR_PITCHER:
            return True
        return False

    def begin_setting_stat(self, response, stat):
        jobs = response.xpath("//table[@class='ind1'][1]/tr")
        for job in jobs:
            if self.get_rid_of_range(job):
                continue
            stat = self.set_stat(job, stat)
        return stat

    def set_stat(self, job, stat):
        data = {}
        data["year"] = job.xpath("td[1]/text()").extract_first()
        data["team"] = job.xpath("td[@class='tm']/text()").extract_first()
        data["number"] = job.xpath("td[@class='seban']/text()").extract_first()
        data["age"] = job.xpath("td[34]/text()").extract_first()
        data["games_played"] = (job.xpath("td[5]/text()").extract_first()
                                if job.xpath("td[5]/text()").extract_first() is not None
                                else job.xpath("td[5]/b/text()").extract_first())
        data["games_started"] = (job.xpath("td[6]/text()").extract_first()
                                if job.xpath("td[5]/text()").extract_first() is not None
                                else job.xpath("td[6]/b/text()").extract_first())
        data["complete_games"] = (job.xpath("td[8]/text()").extract_first()
                                  if job.xpath("td[5]/text()").extract_first() is not None
                                  else job.xpath("td[8]/b/text()").extract_first())
        data["shutouts"] = (job.xpath("td[9]/text()").extract_first()
                            if job.xpath("td[5]/text()").extract_first() is not None
                            else job.xpath("td[9]/b/text()").extract_first())
        data["wins"] = (job.xpath("td[@class='pitcher'][1]/text()").extract_first()
                        if job.xpath("td[@class='pitcher'][1]/text()").extract_first() is not None
                        else job.xpath("td[@class='pitcher'][1]/b/text()").extract_first())
        data["losses"] = (job.xpath("td[@class='pitcher'][2]/text()").extract_first()
                          if job.xpath("td[@class='pitcher'][2]/text()").extract_first() is not None
                          else job.xpath("td[@class='pitcher'][2]/b/text()").extract_first())
        data["saves"] = (job.xpath("td[@class='pitcher'][3]/text()").extract_first()
                         if job.xpath("td[@class='pitcher'][3]/text()").extract_first() is not None
                         else job.xpath("td[@class='pitcher'][3]/b/text()").extract_first())
        data["innings_pitched"] = (job.xpath("td[15]/text()").extract_first()
                                   if job.xpath("td[15]/text()").extract_first() is not None
                                   else job.xpath("td[15]/b/text()").extract_first())
        data["walks"] = (job.xpath("td[20]/text()").extract_first()
                         if job.xpath("td[20]/text()").extract_first() is not None
                         else job.xpath("td[20]/b/text()").extract_first())
        data["hit_by_pitch"] = (job.xpath("td[21]/text()").extract_first()
                                if job.xpath("td[21]/text()").extract_first() is not None
                                else job.xpath("td[21]/b/text()").extract_first())
        data["strikeouts"] = (job.xpath("td[@class='pitcher'][4]/text()").extract_first()
                              if job.xpath("td[@class='pitcher'][4]/text()").extract_first() is not None
                              else job.xpath("td[@class='pitcher'][4]/b/text()").extract_first())
        data["wild_pitches"] = (job.xpath("td[23]/text()").extract_first()
                                if job.xpath("td[23]/text()").extract_first() is not None
                                else job.xpath("td[23]/b/text()").extract_first())
        data["balks"] = (job.xpath("td[24]/text()").extract_first()
                         if job.xpath("td[24]/text()").extract_first() is not None
                         else job.xpath("td[24]/b/text()").extract_first())
        data["batters_faced"] = (job.xpath("td[16]/text()").extract_first()
                                 if job.xpath("td[16]/text()").extract_first() is not None
                                 else job.xpath("td[16]/b/text()").extract_first())
        data["hits"] = (job.xpath("td[18]/text()").extract_first()
                        if job.xpath("td[18]/text()").extract_first() is not None
                        else job.xpath("td[18]/b/text()").extract_first())
        data["home_runs_hit"] = (job.xpath("td[19]/text()").extract_first()
                                 if job.xpath("td[19]/text()").extract_first() is not None
                                 else job.xpath("td[19]/b/text()").extract_first())
        data["runs_scored"] = (job.xpath("td[25]/text()").extract_first()
                               if job.xpath("td[25]/text()").extract_first() is not None
                               else job.xpath("td[25]/b/text()").extract_first())
        data["earns_runs_allowed"] = (job.xpath("td[26]/text()").extract_first()
                                      if job.xpath("td[26]/text()").extract_first() is not None
                                      else job.xpath("td[26]/b/text()").extract_first())
        data["era"] = (job.xpath("td[@class='pitcher'][5]/text()").extract_first()
                       if job.xpath("td[@class='pitcher'][5]/text()").extract_first() is not None
                       else job.xpath("td[@class='pitcher'][5]/b/text()").extract_first())
        data["whip"] = (job.xpath("td[29]/text()").extract_first()
                        if job.xpath("td[29]/text()").extract_first() is not None
                        else job.xpath("td[29]/b/text()").extract_first())
        stat.append(data.copy())
        return stat


class Ohtani(Batter, Pitcher):
    def begin_setting_stat(self, response, stat):
        batter_jobs = response.xpath("//table[@class='ind1'][1]/tr")
        pitcher_jobs = response.xpath("//table[@class='ind1'][2]/tr")
        for batter_job, pitcher_job in zip(batter_jobs, pitcher_jobs):
            if Player.get_rid_of_range(batter_job) or Player.get_rid_of_range(pitcher_job):
                continue
            self.set_stat(batter_job, pitcher_job, stat)
        return stat

    def set_stat(self, batter_job, pitcher_job, stat):
        stat = Batter.set_stat(self, batter_job, stat)
        stat = Pitcher.set_stat(self, pitcher_job, stat)
