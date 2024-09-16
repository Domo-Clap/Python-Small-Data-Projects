import pandas as pd
import plotly.express as px

def basicDFInfo(df):

    print(df.info())

    print(df.columns)

    print(df.shape)

    print(df.head())


def firstNobelPrize(df):

    return df["year"].min()


def latestYear(df):

    return df['year'].max()


def checkDupes(df):

    return df.duplicated().values.any()


def checkNull(df):

    return df.isna().sum()


def convertDates(df):

    df.birth_date = pd.to_datetime(df.birth_date)

    return df.birth_date


def makeDonutChart(df):

    prizeAMNT = df.sex.value_counts()

    fig = px.pie(labels=prizeAMNT.index, values=prizeAMNT.values, names=prizeAMNT.index, title='Num of Male vs Female Winners')

    fig.show()


def getFirst3Females(df):

    return df[df.sex == 'Female'].sort_values('year', ascending=True)[:3]


if __name__ == '__main__':

    nobel_df = pd.read_csv("nobel_prize_data.csv")

    basicDFInfo(nobel_df)

    print(f"First Year Nobel Prize was given out: {firstNobelPrize(nobel_df)}")

    print(f"Latest year in data set: {latestYear(nobel_df)}")

    #print(checkDupes(nobel_df))

    #print(checkNull(nobel_df))

    print(convertDates(nobel_df))

    separated_values = nobel_df.prize_share.str.split('/', expand=True)
    numerator = pd.to_numeric(separated_values[0])
    denomenator = pd.to_numeric(separated_values[1])

    nobel_df['Share_PCT'] = numerator / denomenator

    makeDonutChart(nobel_df)


    print(getFirst3Females(nobel_df))