# How The New York Times is Experimenting with Recommendation Algorithms

Algorithmic curation at The Times is used in designated parts of our website and apps.

The New York Times will publish around 250 articles today, but most readers will only see a fraction of them. The majority of our readers access The New York Times online, not on paper, and often using small devices, which means we have a “real estate” problem: we produce more journalism than we have space to surface to readers at any given time.

To help our readers discover the breadth of our reporting, The Times is experimenting with new ways to deliver more of our journalism to readers. We are building real-time feeds, specialized newsletters and customizable parts of our news app. We are also using recommendation algorithms to highlight articles that are particularly relevant to our readers.

Algorithmic curation at The Times is used in designated parts of our website and apps. We use it to select content where manual curation would be inefficient or difficult, like in the Smarter Living section of the homepage or in Your Weekly Edition, a personalized newsletter. Personalization algorithms are used to complement the editorial judgment that determines what stories lead our news report.

## A contextual recommendation approach

One recommendation approach we have taken uses a class of algorithms called contextual multi-armed bandits. Contextual bandits learn over time how people engage with particular articles. They then recommend articles that they predict will garner higher engagement from readers. The contextual part means that these bandits can use additional information to get a better estimate of how engaging an article might be to a particular reader. For example, they can take into account a reader’s geographical region (like country or state) or reading history to decide if a particular article would be relevant to that reader.

The algorithm we used is based on a simple linear model that relates contextual information—like the country or state a reader is in—to some measure of engagement with each article, like click-through rate. When making new recommendations, it chooses articles more frequently if they have high expected engagement for the given context.

## Using contextual bandits for article recommendations

One model we implemented is a geo-bandit that tries to optimize the expected click-through rate of a set of articles based on the state in which the reader is located. To illustrate this, let’s say we’ve shown two articles—article A and article B—to readers, capturing data about the states that readers were located in and whether they clicked on the articles.

```python
[“recommended”: “article B”; “reader state”: “Texas”, “clicked”: “yes”][“recommended”: “article A”; “reader state”: “New York”, “clicked”: “yes”][“recommended”: “article B”; “reader state”: “New York”, “clicked”: “no”][“recommended”: “article B”; “reader state”: “California”, “clicked”: “no”][“recommended”: “article A”; “reader state”: “New York”, “clicked”: “no”]
```

Once the bandit has been trained on the initial data, it might suggest Article A, Article B or a new article, C, for a new reader from New York. The bandit would be most likely to recommend Article A because the article had the highest click-through rate with New York readers in the past. With some smaller probability, it might also try showing Article C, because it doesn’t yet know how engaging it is and needs to generate some data to learn about it.

Over time, it will get a really good estimate of every article’s click-through rate given every possible location and then mostly show articles it expects to perform best in a given context.

### Why use geographical information?

We chose to use approximate geographical location because it’s one type of contextual information that is readily available in web browsers and apps. While location is not always relevant for news consumption, parts of our report are more relevant to readers in certain parts of the United States or the world.

There are many other types of contextual information, some of which we have implemented. They include a reader’s device type; the time of day where a reader is located; how many stories a reader has viewed in a particular news section, from which we can gauge interest in a particular topic. We have found that depending on the type of articles we’re recommending, different kinds of context variables help the model perform better.

## Choosing the most relevant from Editors’ Picks

We tested a version of the geo-bandit described above in a recommendation module called Editors’ Picks, which shows up in a right-hand column alongside our articles. As the name suggests, editors choose about 30 noteworthy pieces of journalism for the module. We then use a geo bandit to select which particular articles to show to readers based on their location (which we broadly defined by state or region).

Here are some examples of headlines from articles the geo-bandit recommended to readers in different states.

New York
I Know the Struggle’: Why a Pizza Mogul Left Pies at Memorials to 4 Homeless Men
Scientists Designed a Drug for Just One Patient. Her Name Is Mila.
Chasing the Perfect Slice, Bread and Salt in Jersey City Looks to Rome
The Phones Are Alive, With the Sounds of Katie Couric

Texas
When My Louisiana School and Its Football Team Finally Desegregated
This Is an Indian House, According to One Architect
No One Needs a Superyacht, but They Keep Selling Them
The Phones Are Alive, With the Sounds of Katie Couric

Wisconsin
When My Louisiana School and Its Football Team Finally Desegregated
The Phones Are Alive, With the Sounds of Katie Couric
36 Hours in Milwaukee
No One Needs a Superyacht, but They Keep Selling Them

Note how the recommendations include articles that are popular across all of the regions (“The Phones Are Alive, With the Sounds of Katie Couric”), while also capturing different regional interests (“36 Hours in Milwaukee”). By making regionally relevant recommendations, we were able to increase the click-through rate on the Editors’ Picks module by 55 percent, compared to randomly choosing from the pool of articles selected by editors.

## How we implemented contextual bandits

Although the underlying algorithm is relatively simple, contextual bandits can be challenging to implement. Bandits must be continuously re-trained with new data on reader engagement with articles on the Times homepage or apps. This means that not only do we need accurate data on which articles readers read (click data), we need accurate data on what articles were shown to readers (impression data).

Further complicating bandit implementation is the need to do these calculations quickly. As readers visit our page, recommendations need to be made in real-time to avoid blank sections of the page. This real-time requirement also means that any contextual information about the reader has to be made available for our algorithm along with the recommendation request.

Keeping these requirements in mind, we re-train on the most recent data generated by readers interacting with content on our site, and we re-deploy bandit models every 15 minutes. The models are deployed via Kubernetes and training runs are orchestrated using Kubernetes cron jobs. The training data comes from our main event tracking store in BigQuery.

To ensure we have an accurate measurement of what articles were shown to readers, along with data about which articles were read in full, we implemented impression tracking. We found it particularly useful to store a unique ID for every article impression and carry that ID forward whenever a reader clicks on an article. This allows us to join impressions and clicks easily during training.

Using BigTable, we maintain a low-latency store that allows us to quickly access a reader’s recent reading history; We use the articles a reader has read in the past 30 days to build some of the contextual features.

We wrote our contextual bandits in Python, but to ensure they can respond fast enough to meet our latency requirements, we rewrote some of the functionality in Cython, a compiler that translates Python to equivalent C code.

## A recommendation toolbox that helps readers find more stories

Using contextual bandits got us pretty far in terms of increasing reader engagement. But like any algorithm, contextual bandits have strengths and weaknesses. Bandit algorithms are great at quickly adapting to changing preferences and efficiently it exploring new options. A downside is that they are not primarily designed to make recommendations that feel personalized.

Next, we want to combine contextual multi-armed bandits with other models in our recommendation toolbox—like collaborative filtering or content-based recommenders—that include a more fine-grained representation of readers and their interests. By adding outputs of these models as context features to a contextual bandit, we hope to leverage the strength of each approach and get another step closer to our goal of helping our readers discover the coverage most relevant to them.

Anna Coenen is a Senior Data Scientist at The New York Times. She also enjoys plants, cats and cognitive science.
