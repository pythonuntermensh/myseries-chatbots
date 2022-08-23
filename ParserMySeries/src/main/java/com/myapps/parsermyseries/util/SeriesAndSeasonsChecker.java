package com.myapps.parsermyseries.util;

import com.myapps.parsermyseries.entity.NewSeriesEntity;

public class SeriesAndSeasonsChecker {

    public static int Compare(NewSeriesEntity first, NewSeriesEntity second) {

        String firstDescription = first.getDescription();
        String secondDescription = second.getDescription();

        int firstSeason = Integer.parseInt(firstDescription.split("сезон")[0].strip());
        int secondSeason = Integer.parseInt(secondDescription.split("сезон")[0].strip());

        if (firstSeason > secondSeason) return 1;
        else if (firstSeason < secondSeason) return -1;

        int firstSeries = Integer.parseInt(firstDescription.split("сезон")[1].split("серия")[0].strip());
        int secondSeries = Integer.parseInt(secondDescription.split("сезон")[1].split("серия")[0].strip());

        if (firstSeries > secondSeries) return 1;
        else if (firstSeries < secondSeries) return -1;

        return 0;
    }
}
