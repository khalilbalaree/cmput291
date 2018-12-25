import os

def main():
    os.system("sort -u -o adsSorted.txt ads.txt")
    os.system("sort -u -o pdatesSorted.txt pdates.txt")
    os.system("sort -u -o pricesSorted.txt prices.txt")
    os.system("sort -u -o termsSorted.txt terms.txt")

    os.system("perl break.pl < adsSorted.txt > adsTemp.txt")
    os.system("perl break.pl < pdatesSorted.txt > pdatesTemp.txt")
    os.system("perl break.pl < pricesSorted.txt > pricesTemp.txt")
    os.system("perl break.pl < termsSorted.txt > termsTemp.txt")
    """
    os.system("mv recs_temp.txt recs.txt")
    os.system("mv terms_temp.txt terms.txt")
    os.system("mv years_temp.txt years.txt")
    """
    os.system("db_load -c duplicates=0 -T -t hash -f adsTemp.txt ad.idx")
    os.system("db_load -c duplicates=1 -T -t btree -f pdatesTemp.txt da.idx")
    os.system("db_load -c duplicates=1 -T -t btree -f pricesTemp.txt pr.idx")
    os.system("db_load -c duplicates=1 -T -t btree -f termsTemp.txt te.idx")

    os.system("rm adsTemp.txt pdatesTemp.txt pricesTemp.txt termsTemp.txt ads.txt pdates.txt prices.txt terms.txt")

if __name__ == "__main__":
    main()
