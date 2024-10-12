## refs:

https://arxiv.org/abs/2401.17878

## title

A Survey on Data-Centric Recommender Systems

## abstract

Recommender systems (RSs) have become an essential tool for mitigating information overload in a range of real-world applications. Recent trends in RSs have revealed a major paradigm shift, moving the spotlight from model-centric innovations to data-centric efforts (e.g., improving data quality and quantity). This evolution has given rise to the concept of data-centric recommender systems (Data-Centric RSs), marking a significant development in the field. This survey provides the first systematic overview of Data-Centric RSs, covering 1) the foundational concepts of recommendation data and Data-Centric RSs; 2) three primary issues of recommendation data; 3) recent research developed to address these issues; and 4) several potential future directions of Data-Centric RSs.

# Introduction

Recommender systems (RSs) have been widely adopted to alleviate information overload in various real-world applications, such as social media, e-commerce, and online advertising. The past few decades have witnessed the rapid development of recommendation models, evolving from traditional collaborative-filtering-based models Rendle et al. (2009) to more advanced deep-learning-based ones Ge et al. (2023), which have markedly improved the accuracy, diversity, and interpretability of recommendation results Li et al. (2020).

However, as recommendation models are growing larger and increasingly complex, as exemplified by the P5 recommendation model Geng et al. (2022) that integrates five recommendation-related tasks into a shared language generation framework, the primary constraint impacting recommendation performance gradually transitions towards recommendation data. Instead of focusing solely on developing even more advanced models, an increasing number of researchers have been advocating for the enhancement of recommendation data, leading to the emergence of the novel concept of data-centric recommender systems (Data-Centric RSs) Zha et al. (2023).

The fundamental rationale behind Data-Centric RSs is that data ultimately dictates the upper limits of model capabilities. Large and high-quality data constitutes the essential prerequisite for breakthroughs in performance. For instance, the remarkable advancements of GPT models in natural language processing are mainly originated from the use of huge and high-quality datasets Ouyang et al. (2022). Similarly, in computer vision, convolutional neural networks exhibit performance on par with vision transformers when they have access to web-scale datasets Smith et al. (2023). For RSs, the implication is clear: the greater the quality Wang et al. (2021a) and/or the quantity Liu et al. (2023) of recommendation data, the more proficiently RSs can characterize user preferences, resulting in recommendations that resonate well with users.

Despite considerable attention from researchers and a great variety of methods that have been put forth in Data-Centric RSs, to the best of our knowledge, there has been no effort to gather and provide a summary of works in this promising and fast-developing research field. To fulfill this gap, we conduct a systematic review of the literature on Data-Centric RSs and provide insights from the following four aspects. We first detail the specifics of data that could be used for recommendation and present the formalization of Data-Centric RSs (Section 2). Next, we identify three key issues in recommendation data, i.e., data incompleteness, data noise, and data bias (Section 3), and categorize the existing literature in accordance with these issues (Section 4). Finally, we spotlight a number of encouraging research directions in Data-Centric RSs (Section 5).

![figure1]()

# Formulation

## Recommendation Data

The goal of RSs is to help users discover potential items of interest and then generate personalized recommendations. To achieve this goal, as shown in Figure 1, we summarize three types of data that can be used in RSs:

• User profiles: User profiles refer to a collection of information and characteristics that describe an individual user. In the context of recommendation, user profiles typically include demographics, preferences, behavior patterns, and other relevant data that helps define and understand a user’s characteristics, needs, and interests.
• Item attributes: Item attributes involve the specific details or characteristics that describe an item. These details can include color, material, brand, price, and other relevant information that helps identify or categorize the item.
• User-item interactions: User-item interactions represent users’ actions or involvements with items. Additional contextual information such as ratings, behaviors, timestamps, and reviews can also be utilized to provide a more comprehensive picture of the interactions between users and items.

![figure2]()

## Data-Centric RSs

As shown in Figure 2, different from Model-Centric RSs which improve recommendation performance by refining models, Data-Centric RSs shift the focus from model to data and emphasize the importance of data enhancement. More specifically, given the recommendation data 𝒟 (e.g., user-item interactions), Data-Centric RSs aim to determine a strategy � , which takes the original data 𝒟 as input and outputs the enhanced data 𝒟 ′ :

$$
\tag{1}
$$

The enhanced data 𝒟 ′ could be used by different recommendation models to further improve their performance. We also attempt to answer the following questions to clarify the definition of Data-Centric RSs: Q1: Are Data-Centric RSs the same as Data-Driven RSs? Data-Centric RSs and Data-Driven RSs are fundamentally different, as the latter only emphasize the use of recommendation data to guide the design of recommendation models without modifying the data, which are essentially still Model-Centric RSs Zha et al. (2023). Q2: Why Data-Centric RSs are necessary? The objective of a recommendation model is to fit the recommendation data. Without changing the data, Model-Centric RSs may generalize or even amplify errors (e.g., noise or bias) in the data, resulting in suboptimal recommendations Zhang et al. (2023a). Therefore, Data-Centric RSs are necessary. Q3: Will Data-Centric RSs substitute Model-Centric RSs? Data-Centric RSs do not diminish the value of Model-Centric RSs. Instead, these two paradigms complement each other to build more effective recommender systems. Interestingly, model-centric methods can be used to achieve data-centric goals. For example, diffusion models Liu et al. (2023) can be an effective tool for data augmentation. Data-centric methods can facilitate the improvement of model-centric outcomes. For instance, high-quality synthesized data could inspire further advancements in model design Sachdeva et al. (2022).

![figure3]()

# Data Issues

As illustrated in Figure 3, we identify three key issues from which recommendation data may suffer, including data incompleteness, data noise, and data bias.

## Data Incompleteness

The data incompleteness issue refers to the scenarios where data used for making recommendations is inadequate, consequently resulting in information gaps or missing details regarding users or items. Specifically, the forms and reasons in which recommendation data can be incomplete include:

• Missing user profiles: During the registration or setup process, users may fail to fully complete their profiles. Key information may be omitted as they might bypass certain fields or provide inadequate information Wei et al. (2023). For example, a user may neglect to add age or gender, resulting in a profile that is less informative than it could be.
• Limited item attributes: Similarly, data regarding item attributes may also be lacking. This incompleteness hinders the ability to precisely portray items and capture their distinct characteristics Wu et al. (2020). For instance, an online bookshop may only provide basic data about a book such as the title and author, neglecting additional details like genre or publication year that can enhance the recommendation accuracy.
• Sparse user-item interactions: RSs can encounter the “cold start” problem when new users join. With limited or no historical interactions for these users, providing accurate recommendations becomes challenging Wang et al. (2019). Additionally, users usually do not engage with every item. For example, in a movie recommender system, a user may only rate a handful of thousands of movies available, leading to an incomplete picture of true preferences.
• Inadequate contextual information: Contextual information like timestamps, ratings, locations, or user reviews significantly contributes to generating effective recommendations. However, due to privacy issues or constraints in user feedback, the available contextual information may be incomplete or lack details Chae et al. (2019). For instance, a user might give a high rating for a hotel visit but does not provide a review that could offer useful insights about his/her preferences for future recommendations.

## Data Noise

Data noise arises when a portion of the recommendation data is irrelevant or erroneous, which negatively impacts the quality of recommendations provided. Noisy recommendation data can appear in several forms:

• Redundant data: An abundance of identical data is often the consequence of errors during the data collection process. RSs might incorrectly identify and log certain identical item attributes multiple times, such as the same item category appearing repeatedly. Alternatively, it might record a user interacting with the same item multiple times – a shop page refresh mistake, for example.
• Inconsistent data: Inconsistencies in data occur mainly due to human errors, such as users unintentionally clicking or providing incorrect ratings to an item Lin et al. (2023b). Additionally, different data sources, like explicit ratings, implicit signals, and textual reviews, can present conflicting information about a user’s current preferences. For example, a user might provide a low rating for a product, but the text in his/her review might be generally positive, which creates confusion.
• Spam or fake data: At a more malicious level, RSs can be susceptible to spam or fake data generated by either malicious users or automated bots trying to harm the system. This undesired data can significantly contaminate the pool of authentic user data and can drastically impact the quality of recommendations, leading to decreased user satisfaction Wu et al. (2023). A typical example is “review bombing”, where orchestrated attempts by certain users or bots fill a product’s review section with negative feedback to harm its overall rating, even though the product may be generally well-received by the majority.

![figure4]()

## Data Bias

A significant data bias issue arises when there is a significant distribution shift between the data collected and the real-world data. This problem mainly originates from:

• Shifts in user preferences: As illustrated in Figure 4, users’ preferences can change due to shifts in wider environmental factors or their personal circumstances like pregnancy. In these scenarios, data collected in the past may no longer provide an accurate representation of the user’s current preferences Wang et al. (2023a).
• Changes in item popularity: Similarly, the popularity of certain items or categories is not static and can significantly vary over time. Items or trends that were once prevalent may lose their charm and relevance as time passes. For example, as shown in Figure 4, a certain genre of products like the watch that was the rage a few years ago may not hold the same appeal to the audience in the present day as tastes evolve and new genres emerge Zhang et al. (2023a).

![Table 1:Representative works and key techniques used in handling different data issues]()

# Research Progress

We organize the existing literature according to the data issues in RSs outlined before. Specific categorization as well as representative works and techniques are shown in Table 1.

## Handling Incomplete Data

The key to handling incomplete data is to fill in the missing information. According to the different forms of incomplete data introduced in Section 3.1, we divide existing methods into two categories: attribute completion and interaction augmentation.

### Attribute Completion

Let 𝒱 be the set of users and items. In practice, the profiles or attributes of some users or items may not be available. Therefore, the set 𝒱 can be divided into two subsets, i.e., 𝒱 + and 𝒱 − , which denote the attributed set and the no-attribute set, respectively. Let 𝒜 = { � � ∣ � ∈ 𝒱 + } denote the input attribute set. Attribute completion aims to complete the attribute for each no-attribute user or item � ∈ 𝒱 − :

$$
\tag{2}
$$

where � � � denotes the completed attribute of � . The enhanced input attribute set 𝒜 ′ is formulated as:

$$
\tag{}
$$

Existing works on attribute completion mainly rely on utilizing the topological structure of given graphs (e.g., user-item interaction, knowledge graphs, and social networks) Wu et al. (2020); You et al. (2020); Jin et al. (2021); Tu et al. (2022); Zhu et al. (2023); Guo et al. (2023). For instance, by modeling user-item interactions with respective user or item attributes into an attributed user-item bipartite graph, AGCN Wu et al. (2020) proposes an adaptive graph convolutional network for joint item recommendation and attribute completion, which iteratively performs two steps: graph embedding learning with previously learned attribute values, and attribute update procedure to update the input of graph embedding learning. Moreover, given a knowledge graph, HGNN-AC Jin et al. (2021) leverages the topological relationship between nodes as guidance and completes attributes of no-attribute nodes by weighted aggregation of the attributes of linked attributed nodes. AutoAC Zhu et al. (2023) identifies that different attribute completion operations should be taken for different no-attribute nodes and models the attribute completion problem as an automated search problem for the optimal completion operation of each no-attribute node. Instead of focusing on attribute completion accuracy, FairAC Guo et al. (2023) pays attention to the unfairness issue caused by attributes and completes missing attributes fairly.

Given the extensive knowledge base and powerful reasoning capabilities of large language models (LLMs) Zhao et al. (2023), some recent works have focused on leveraging LLMs to complete missing attributes. For example, LLMRec Wei et al. (2023) carefully designs some prompts as the inputs of ChatGPT Ouyang et al. (2022) to generate user profiles or item attributes that were not originally part of the dataset. An example of designed prompts is as follows:

> Provide the inquired information of the given movie. Heart and Souls (1993), Comedy/Fantasy The inquired information is: director, country, language. Please output them in form of: director, country, language

Similar to FairAC, some works [Xu et al., 2023] are exploring the ability of LLMs in generating sensitive user profiles or item attributes and considering the risks it may bring to privacy leakage and unfairness issues.

### Interaction Augmentation

Let 𝒪 = { ( � , � ) ∣ � , � ∈ 𝒱 } be the set of user-item pair ( � , � ) with observed interactions. We denote ℛ = { � � , � ∣ ( � , � ) ∈ 𝒪 } as the input interaction set. For inactive users and unpopular items, insufficient observed interactions can lead to inaccurate characterization of user preferences and item features. Therefore, interaction augmentation aims to augment the interaction information of some specific unobserved user-item pairs ( � , � ) ∉ 𝒪 :

$$
\tag{3}
$$

where � � , � � denotes the augmented interaction information of ( � , � ) . The enhanced input interaction set ℛ ′ is:

$$
\tag{}
$$

![figure5]()

For implicit information such as like/dislike, the critical focus of interaction augmentation lies in how to choose an interaction. Negative sampling pays attention to how to choose an interaction as dislike Rendle et al. (2009); Zhang et al. (2013); Chen et al. (2017); Ding et al. (2020); Huang et al. (2021); Lai et al. (2023); Shi et al. (2023); Lai et al. (2024). Specifically, negative sampling aims to identify uninteracted items of a user as negative items. The simplest and most prevalent idea is to randomly select uninteracted items, BPR Rendle et al. (2009) is a well-known instantiation of this idea. Inspired by the word-frequency-based negative sampling distribution for network embedding Mikolov et al. (2013), NNCF Chen et al. (2017) adopts an item-popularity-based sampling distribution to select more popular items as negative. DNS Zhang et al. (2013) proposes to select uninteracted items with higher prediction scores (e.g., the inner product of a user embedding and an item embedding). Such hard negative items can provide more informative training signals so that user interests can be better characterized. SRNS Ding et al. (2020) oversamples items with both high predicted scores and high variances during training to tackle the false negative problem. DENS Lai et al. (2023) points out the importance of disentangling item factors in negative sampling and designs a factor-aware sampling strategy to identify the best negative item. MixGCF Huang et al. (2021) synthesizes harder negative items by mixing information from positive items while AHNS Lai et al. (2024) proposes to adaptively select negative items with different hardness levels.

Different from negative sampling, positive augmentation focuses on how to choose an interaction as like Wang et al. (2019, 2021b); Yang et al. (2021); Zhang et al. (2021a); Lai et al. (2022); Liu et al. (2023); Wei et al. (2023). For example, EGLN Yang et al. (2021) selects uninteracted items with higher prediction scores and labels them as positive to enrich users’ interactions. CASR Wang et al. (2021b) leverages counterfactual reasoning to generate user interaction sequences in the counterfactual world. MNR-GCF Lai et al. (2022) constructs heterogeneous information networks and fully exploits the contextual information therein to identify potential user-item interactions. Based on generative adversarial nets (GANs), AugCF Wang et al. (2019) generates high-quality augmented interactions that mimic the distribution of original interactions. Inspired by the superior performance of diffusion models in image generation, DiffuASR Liu et al. (2023) adapts diffusion models to user interaction sequence generation, and a sequential U-Net is designed to capture the sequence information and predict the added noise of generated interactions. Leveraging the capabilities of LLMs, LLMRec Wei et al. (2023) also seeks to identify both positive and negative interactions from a candidate set using well-designed prompts.

For contextual information like rating, the critical focus of interaction augmentation shifts to how to infer the missing value Ren et al. (2012, 2013); Yoon et al. (2018); Chae et al. (2019); Li et al. (2019); Chae et al. (2020); Hwang and Chae (2022). For instance, AutAI Ren et al. (2012) and AdaM Ren et al. (2013) calculate missing ratings according to heuristic similarity-based metrics, such as Pearson correlation coefficient or cosine similarity. RAGAN Chae et al. (2019) and UA-MI Hwang and Chae (2022) leverage GANs for rating augmentation. Instead of augmenting ratings of interactions between real users and items, AR-CF Chae et al. (2020) proposes to generate virtual users and items and then adopts GANs to predict ratings between them.

### Discussion

While a variety of methods exist for addressing the incomplete data issue, the fact remains that no single method is capable of comprehensively addressing all scenarios involving missing data. Consequently, a considerable amount of time and effort must be devoted to identifying missing information and selecting enhancement strategies. Furthermore, evaluating the quality of enhanced data is not straightforward – improvements in RSs might be misleadingly attributed to the simple expansion of data volume, which can cloud the actual effects of refinements in data quality.

## Handling Noisy Data

The key to handling the data noise issue is to filter out the noisy information. According to the varying severity of noisy data presented in Section 3.2, we divide existing denoising methods into three categories: reweighting-based methods, selection-based methods, and dataset distillation/condensation, which are illustrated in Figure 5.

### Reweighting-Based Denoising

The reweighting-based method aims to assign lower weights to the noisy data (or assign higher weights to the noiseless data) Wang et al. (2021a); Gao et al. (2022); Zhou et al. (2022); Zhang et al. (2023d); Ge et al. (2023); Wang et al. (2023c). Wang et al. Wang et al. (2021a) experimentally observe that noisy interactions are harder to fit in the early training stages, and, based on this observation, they regard the interactions with large loss values as noise and propose an adaptive denoising training strategy called R-CE, which assigns different weights to noisy interactions according to their loss values during training. SLED Zhang et al. (2023d) identifies and determines the reliability of interactions based on their related structural patterns learned on multiple large-scale recommendation datasets. FMLP-Rec Zhou et al. (2022) adopts learnable filters for denoising in sequential recommendation. The learnable filters perform a fast Fourier transform (FFT) to convert the input sequence into the frequency domain and filter out noise through an inverse FFT procedure. SGDL Gao et al. (2022) leverages the self-labeled memorized data as guidance to offer denoising signals without requiring any auxiliary information or defining any weighting functions. AutoDenoise Ge et al. (2023) adopts reinforcement learning to automatically and adaptively learn the most appropriate weight for each interaction.

### Selection-Based Denoising

Instead of assigning lower weights, the selection-based method directly removes the noisy data Tong et al. (2021); Wang et al. (2021a); Yuan et al. (2021); Zhang et al. (2022b); Lin et al. (2023a); Zhang et al. (2023c); Quan et al. (2023); Wang et al. (2023b); Lin et al. (2023b). For instance, different from R-CE, Wang et al. Wang et al. (2021a) propose another adaptive denoising training strategy called T-CE, which discards the interactions with large loss values. RAP Tong et al. (2021) formulates the denoising process as a Markov decision process and proposes to learn a policy network to select the appropriate action (i.e., removing or keeping an interaction) to maximize long-term rewards. DSAN Yuan et al. (2021) suggests using the entmax function to automatically eliminate the weights of irrelevant interactions. HSD Zhang et al. (2022b) learns both user-level and sequence-level inconsistency signals to further identify inherent noisy interactions. DeCA Wang et al. (2023b) finds that different models tend to make more consistent agreement predictions for noise-free interactions, and utilizes predictions from different models as the denoising signal. GDMSR Quan et al. (2023) designs a self-correcting curriculum learning mechanism and an adaptive denoising strategy to alleviate noise in social networks. STEAM Lin et al. (2023b) further designs a corrector that can adaptively apply “keep”, “delete”, and “insert” operations to correct an interaction sequence.

Some studies integrate the reweighting-based method with the selection-based method for better denoising Tian et al. (2022); Ye et al. (2023). For instance, RGCF Tian et al. (2022) and RocSE Ye et al. (2023) estimate the reliability of user-item interactions using normalized cosine similarity between their respective embeddings. Subsequently, they filter out interactions and only retain those whose weights exceed a pre-defined threshold value.

### Dataset Distillation/Condensation

Dataset distillation or dataset condensation techniques Yu et al. (2023) aim to synthesize data points with the goal of condensing the comprehensive knowledge from the entire dataset into a small, synthetic data summary. This process retains the essence of the data, enabling models to be trained more efficiently. Recently, some works Sachdeva et al. (2022); Wu et al. (2023) observe that dataset distillation has a strong data denoising effect in recommendation. For example, DISTILL-CF Sachdeva et al. (2022) applies dataset meta-learning to synthetic user-item interactions. Remarkably, models trained on the condensed dataset synthesized by DISTILL-CF have demonstrated improved performance compared to those trained on the full, original dataset.

### Discussion

Normally, data collected from real-world scenarios are frequently contaminated with noise stemming from system bugs or user mistakes. However, obtaining labels for this noise is often impractical or even impossible, due to the lack of expert knowledge required for identifying noise, the high costs associated with manual labeling, or the dynamic nature of some noise which makes it hard to give fixed labels. In the absence of the ground truth, it is difficult to determine whether the denoising method achieves the optimal situation – no over-denoising or under-denoising. Taking into account this limitation, it may be preferable to synthesize a noise-free dataset via dataset distillation/condensation rather than attempting to adjust or filter the existing dataset through reweighting-based or selection-based methods.

## Handling Biased Data

The key to handling biased data is to align the biased training distribution with the unbiased test distribution. According to the causes of biased data explained in Section 3.2, we divide existing debiasing methods into two categories: user preference alignment and item popularity alignment.

### User Preference Alignment

User preferences may shift due to a variety of reasons, such as temporal changes Zafari et al. (2019); Wangwatcharakul and Wongthanavasu (2021); Ding et al. (2022), locational moves Yin et al. (2016), or alterations in personal and environmental conditions Zheng et al. (2021); He et al. (2022); Wang et al. (2023a). Existing methods are designed to track and adjust to these changes, thereby maintaining alignment with the ever-evolving user preferences. For example, Aspect-MF Zafari et al. (2019) analyzes and models temporal preference drifts using a component-based factorized latent approach. MTUPD Wangwatcharakul and Wongthanavasu (2021) adopts a forgetting curve function to calculate the correlations of user preferences across time. ST-LDA Yin et al. (2016) learns region-dependent personal interests and crowd preferences to align locational preference drifts. Wang et al. Wang et al. (2023a) review user preference shifts across environments from a causal perspective and inspect the underlying causal relations through causal graphs. Based on the causal relations, they further propose the CDR framework, which adopts a temporal variational autoencoder to capture preference shifts.

### Item Popularity Alignment

Existing methods for item popularity alignment roughly fall into five groups Zhang et al. (2023a). Inverse propensity scoring Schnabel et al. (2016); Saito et al. (2020) utilizes the inverse of item popularity as a propensity score to rebalance the loss for each user-item interaction. Domain adaptation Bonner and Vasile (2018); Chen et al. (2020) leverages a small sample of unbiased data as the target domain to guide the training process on the larger but biased data in the source domain. Causal estimation Wei et al. (2021); Zhang et al. (2021b); Wang et al. (2022) identifies the effect of popularity bias through assumed causal graphs and mitigates its impact on predictions. Regularization-based methods Boratto et al. (2021) explore regularization strategies to adjust recommendation results, aligning them more closely with the actual popularity distribution. Generalization methods Zhang et al. (2022a, 2023b, 2023a) aim to learn invariant features that counteract popularity bias, thereby enhancing the stability and generalization capabilities of recommendation models.

### Discussion

Traditional evaluation settings in RSs may not be appropriate for assessing debiasing methods because they typically entail that the distribution of a test set is representative of the distribution in the training set (independent and identically distributed evaluation settings). Therefore, in this part, we discuss two out-of-distribution evaluation settings to assess debiasing methods:

• Temporal split setting: Temporal split setting slices the historical interactions into the training, validation, and test sets according to the timestamps Zhang et al. (2022a, 2023b). In this case, any shift in user preferences or item popularity over time is appropriately represented and accounted for during the evaluation.
• Popularity split setting: Popularity split setting constructs the training, validation, and test sets based on various popularity distributions Wei et al. (2021); Zheng et al. (2021). For example, the training interactions are sampled to be a long-tail distribution over items while the validation and test interactions are sampled with equal probability in terms of items (uniform popularity distribution). However, such a split setting has an inherent drawback: it may inadvertently lead to information leakage. By explicitly tailoring the test set to a known distribution of item popularity, the debiasing methods might be unduly influenced by this information.

# Future Directions

## Data-Centric RSs with Multimodal Data

Multimodal data refers to data that consists of multiple modalities or types of information, such as text, images, audio, video, or any combination thereof. Traditionally, RSs have primarily relied on user-item interaction data, such as ratings or click-through data, to generate recommendations. By incorporating multimodal data, RSs can capture richer and more diverse user preferences and item characteristics, leading to more personalized and relevant recommendations Truong and Lauw (2019). However, the data issues mentioned before (i.e., incomplete data, noisy data, and biased data) also exist in multimodal data, and they can pose additional challenges in the context of multimodal RSs:

• Heterogeneity: Multimodal data can be highly heterogeneous, with different modalities having distinct data formats, scales, and distributions. For example, text data may require natural language processing techniques, while image data may need computer vision algorithms.
• Imbalance: Multimodal datasets may exhibit imbalances in the distributions of different modalities. For example, there may be a larger number of text samples compared to images or audio samples. Modality imbalance can affect the performance and generalization of recommendation models trained on such data.
• Scalability: Multimodal data, especially when it includes high-dimensional modalities like images or videos, can be computationally expensive to process and analyze. Therefore, handling large-scale multimodal data may require efficient algorithms or distributed computing frameworks to ensure scalability.

## Data-Centric RSs with LLMs

With the emergence of large language models (LLMs) in natural language processing, there has been a growing interest in harnessing the power of these models to enhance recommender systems. In Data-Centric RSs, LLMs can serve as:

• Recommendation models: Pre-trained LLMs can take as input a sequence that includes user profiles, item attributes, user-item interactions, and task instructions. Then LLMs analyze this information to understand the context and the user’s preferences. Based on this understanding, LLMs can generate a sequence that directly represents the recommendation results, which could be a list of items, a ranking of items, or even detailed descriptions or reasons for the recommendations. However, using LLMs as recommendation models also raises some challenges such as limited token length or latency, especially for users with a large amount of interactions. With data denoising techniques to improve the design of input sequences, the ability of LLMs as recommendation models can be further explored.
• Data processors: As mentioned before, given the extensive knowledge base and powerful reasoning capabilities of LLMs, some recent work has attempted to augment data with LLMs, for example, through carefully designed prompts, LLMRec Wei et al. (2023) employs three simple yet effective LLM-based data augmentation strategies to augment implicit feedback, user profiles, and item attributes, respectively. Moving forward, it’s crucial to investigate the capability of LLMs in managing tasks such as data denoising and data debiasing. This could pave the way for LLMs to harmonize Data-Centric RSs effectively.

## Automatic Data-Centric RSs

Automatic machine learning (AutoML) He et al. (2021) refers to the process of automating the end-to-end process of applying machine learning to real-world problems, which typically involves automating a variety of tasks that are part of the machine learning workflow. In the context of Data-Centric RSs, these tasks encompass data augmentation, data denoising, and data debiasing. Consequently, AutoML can automatically streamline and enhance the efficiency of these tasks, enabling more accurate recommendations, which is of great significance in practice.

## Transparent Data-Centric RSs

Transparent Data-Centric RSs refer to Data-Centric RSs that not only offer enhanced data for model training but also provide insights into how and why particular enhancements are made, thereby allowing users and developers to understand the underlying decision-making processes. Research in transparent Data-Centric RSs is tackling complex challenges, such as the trade-off between transparency and complexity, ensuring user privacy while providing explanations, and developing standards for explainability and interpretability.

# Conclusion

In this survey, we presented a comprehensive literature review of Data-Centric RSs. We systematically analyzed three critical issues inherent in recommendation data and subsequently categorized existing works in accordance with their focus on these issues. Additionally, we point out a range of prospective research directions to advance Data-Centric RSs. We expect that this survey can help readers easily grasp the big picture of this emerging field and equip them with the basic techniques and valuable future research ideas.
