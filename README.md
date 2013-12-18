boxoffice
=========

Predicting audience film ratings of movies using machine learning.
-----

This project explores machine learning methods for predicting the audience ratings of movies. The process of selecting and extracting features for each movie in a corpus of samples is discussed. In particular, methods for converting symbolic film features, such as cast members and directors, into numerical values are presented. The results of several regression algorithms are discussed. This approach can be used to predict the success of movies, as characterized by audience ratings, based solely on primitive features, such as the choice of director, genre, and cast with an average error of approximately 10%.

An example of the regression results

![average regression error over 100 iterations] (https://raw.github.com/SharangP/boxoffice/master/code/Figures/avgerror.png)

Our results can be reproduced by running the following command:

```
python regression.py
```

The complete process of building the database and aggregating features can be initiated with the following commands:

```
python scrape.py
python actors.py
python agg_people.py
python agg_genre.py
python getfeatures.py
```
