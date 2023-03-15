import sys, os
sys.path.append("D:\\Coding Projects\\Arcadia Projects\\arcadia-tweet-notifier")
from tweepy import StreamingClient, StreamRule
from dotenv import load_dotenv
from helpers.tweepyClient import getTweepyClient

from classes.TweetPrinterV2 import TweetPrinterV2

load_dotenv()


class TweetStreamer:

    def __init__(self, list1, list2, list3, list4, BEARER_TOKEN):
        self.accountsList1 = list1
        self.accountsList2 = list2
        self.accountsList3 = list3
        self.accountsList4 = list4
        self.BEARER_TOKEN = BEARER_TOKEN
        self.tweetPrinter = TweetPrinterV2(BEARER_TOKEN)

    def cleanRules(self):
        ruleIds = []
        rules = self.tweetPrinter.get_rules()
        rulesArr = rules.data
        if rulesArr != None:
            for rule in rulesArr:
                print(f"rule marked to delete: {rule.id} - {rule.value}")
                ruleIds.append(rule.id)

            if len(ruleIds) > 0:
                self.tweetPrinter.delete_rules(ruleIds)
                self.tweetPrinter = TweetPrinterV2(self.BEARER_TOKEN)
            else:
                print("no rules to delete")

    def ruleString(self, flag):
        index = 0
        ruleString = ""
        if flag == 1:
            ruleString = '''from: 1001414496819261440 OR from: 1347335187823292416 OR from: 1190283145 OR from: 25071910 OR from: 1411274211444854785 OR from: 1352089119334281216 OR from: 1350996311777161219 OR from: 1297920445979807744 OR from: 784068635958644736 OR from: 1424441728770220037 OR from: 1085046365523066880 OR from: 1138033434 OR from: 1103404363861684236 OR from: 971741153530757120 OR from: 809002141838876673'''
        elif flag == 2:
            ruleString = '''from: 965137759731003392 OR from: 1517328801205833731 OR from: 1354400126857605121 OR from: 1534084530763894784 OR from: 972970759416111104 OR from: 1962290894 
                            OR from: 2335075836 OR from: 813674916784418817 OR from: 1008162403 OR from: 1554869999919108096 OR from: 1582601037550325760 OR from: 1260953582897111042 OR from: 6450372 OR from: 826381583489855490 OR from: 1139174563802226688'''
        elif flag == 3:
            ruleString = '''from: 1225636783418830848 OR from: 1529009920187809792 OR from: 1292201662531211264 OR from: 1511052636988051464 OR from: 1451314985292939268 OR from: 1318528773969616897 OR from: 473622999 OR from: 897920537971871744 OR from: 1424441728770220037 OR from: 319980816 OR from: 1456891312230506496 OR from: 1576165268497244163 OR from: 1231038340616478720 OR from: 951854237276876801 OR from: 1411778399073443840 OR from: 1414218305343209477'''

        elif flag == 4:
            ruleString = '''from: 1414218305343209477 OR from: 1623236872402083841 OR from: 1448734133400842243 OR from: 1435842469971771393 OR from: 178652396 OR from: 1582601037550325760 OR from: 234748308 OR from: 2966287497'''

        print()
        print(ruleString)
        print()
        return ruleString

    def startStreaming(self):
        self.cleanRules()
        rules = []
        rules.append(StreamRule(self.ruleString(1)))
        rules.append(StreamRule(self.ruleString(2)))
        rules.append(StreamRule(self.ruleString(3)))
        rules.append(StreamRule(self.ruleString(4)))
        print(rules)
        self.tweetPrinter.add_rules(rules)
        self.tweetPrinter.filter(expansions="author_id", tweet_fields="created_at")
