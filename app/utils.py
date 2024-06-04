import main1, main2

# from . import main1
# from . import main2

def test(**kwargs):
    string = "hcmut/iaslab/nlp/data/rule.xlsx"
    number_of_sentences = 1000
    main1.part_1(string)
    main1.part_2(string, number_of_sentences)
    main1.part_3(string)
    main2.main()

if __name__ == "__main__":
    test()
    