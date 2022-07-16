---
marp: true
theme: gaia
_class: lead
paginate: true
backgroundColor: #fff
backgroundImage: url('https://marp.app/assets/hero-background.svg')
header: Collider bias
# footer: 2022, 5, 17 Morita
style: |
  section.title * , h1{
      text-align: center;
  }
---

<!-- ![bg left:50% 80%](因果ダイアグラム.drawio.png) -->

![bg 50% opacity:.3](因果ダイアグラム.drawio.png)

# **Collider Bias**

### 合流点バイアス

### Things to keep in mind when you want to discuss "Causal Relation" through regression analysis:part 2

回帰分析を通して因果関係を議論したい時に注意すべきこと:part 2

2022/05/08 Whole seminar
Masato MORITA

---

# First of all, **Why I chose this topic**??

### 1. I have the impression that more and more members are using regression analysis in their research activities these days.

### 2. I recently read a book on statistical causal inference and learned how to analyze causality using regression analysis, so I want to share some information a little bit...!

---

# Today's My Objective

I want to share one of the idea of **Statistical Causal Inference (統計的因果推論)**:

- One of the application fields of statistics and machine learning.
- The aim of this field is analysing causal relation from observed dataset.

---

# Today's My Objective

#### (Dear user of regression analysis)

###### I want to share **what we should careful when interpreting the value of regression coefficient** from viewpoint of causal inference.

#### (Dear not user of regression analysis)

###### I want to share **the patterns that may mislead us** when discussing causal relation based on observed data.

---

# Outline

### 1. Review:Correlation vs Causation, Confounding

(復習)相関関係vs因果関係、交絡

### 2. When is **regression coefficients** different from **causal effects**? part 2: collider bias

どの場合に回帰係数の値と因果効果の値がズレる？part 2: 合流点bias

---

<!-- _class: title -->

# 1. Review:Correlation vs Causation, Confounding

(復習)相関関係vs因果関係、交絡

---

# What is Causal Relation(因果関係)?

#### - The definition of causal relation is ...

###### In case that **"when factor X is changed (intervention), factor Y also changes,"** we can say "there is a **causal relationship of factor X → factor Y**

- The difference with correlation is ...
  ![w: h:9cm](relations_3kinds.png)

---

# What is Causal Effect(因果効果)?

#### - The definition of causal relation is ...

###### In case that **"when factor X is changed (intervention), factor Y also changes**," we can say "there is a **causal relationship of factor X → factor Y**

In above case,

##### - X: "cause"(原因変数), Y: "outcome"(結果変数)

##### - "**causal effect(intervention effect)** of $X \Rightarrow Y$" :Average change of Y when X is changed by one unit

#### In Causal Inference, one motivation is quontification of causal effect.

---

# What is Linear Regression Analysis?

It's a little bit mathematical.

$$
\mathbf{y} = f(\mathbf{x_1}, \cdots, \mathbf{x}_k) + \mathbf{\epsilon}\\
= \beta_0 + \beta_1 \mathbf{x}_1 + \cdots + \beta_k \mathbf{x}_k + \mathbf{\epsilon}
= \mathbf{\beta}X + \mathbf{\epsilon}
$$

where is ...

###### $\mathbf{y}$ : (in Causal Inference, it should be "outcome")

###### $X$ : (in Causal Inference, it should include "cause")

###### $\mathbf{\beta}$ : the regression coefficent of $X$.

###### $\mathbf{\epsilon}$ : Probabilistic component of y。

---

# the usage of Regression analysis

the usage of Regession analysis is separated mainly three objectives:

![w: h:8cm](objectives_of_regression_analysis.png)

from viewpoint of "Causal Inference", regression analysis is utilized for "**Description**" and "**Control/Intervention**".

---

# Example: height=>weight

$$
\text{weight} = \beta_0 + \beta_1 \times \text{height} + \epsilon \\
\Rightarrow \beta_1 = 0.34 (p = 0.00)
$$

###### In this case, $\beta_1$ can be interpret 'causal effect' of 'height' $\Rightarrow$ 'weight'.

###### However, the value of the regression coefficient **does not necessarily fit** with the causal effect.

![bg left:50% 90%](height_x_weight_y_with_LRline.png)

---

# 2. When is **regression coefficients** different from **causal effects**?

there are mainly 4 cases :

### 1. Direction of causation is opposite

### 2. **Confounding**

### 3. Collider Bias

### 4. Intermediate variables are included

---

# Summary of my last short lecture

##### - Correlation $\neq$ Causation(Causal relation)

##### - When discussing causal relation from observational data, we should consider **confounding factors**.

##### - When estimating causal effects from regression coefficients in regression analysis, we should **check confounding factors** and **add them to the explanatory variables**.

---

# However...

###### So, according to my last short lecture...

#### we should **add factors that seem to be related to X(cause) & Y(outcome) to the model** as explanatory variables"...??

###### However...but...in actual... I am afraid that...

#### Sometimes, because of adding factors that seems to be related to the X(cause) & Y(outcome), "regression coefficients $\neq$ causal effects"(i.e. Suprious Correlation 疑似相関) is happened.

---

# 2. When is **regression coefficients** different from **causal effects**?

there are mainly 4 cases :

### 1. Direction of causation is opposite

### 2. Confounding

### 3. **Collider Bias(合流点バイアス)**

### 4. Intermediate variables are included

---

## What is "collider bias" (合流点バイアス)??

#### "collider" is ...

##### here, in these causal diagrams, factor B is called "collider(合流点)" of X and Y:

#### "collider bias(合流点バイアス)" is ...

###### the bias(偏り) caused by **selecting(選択)/ stratifing(層別化)/ adjusting(調整) data at the "collider"** of cause(X) and effect(Y) in the process of data collection or analysis.

![bg right:35% 90%](causal_diagram_collider.drawio.png)

---

## Example of "collider bias"(in data collection)

### Let's imagine the case of "enviromnental subsidy (環境補助金)" based on CO2 emission & TMR of a car!

<!-- 我々は地方自治体の環境グループ。この地方自治体では、企業の"環境負荷低減"の取り組みを推奨する為に補助金制度を設定している。補助金付与の可否は、CO2排出量とTMRの2つの指標に基づいて判定される。-->

###### - We are the member of environmental group of a government.
###### - We has set up **a environmental subsidy(環境補助金)  for automobile makers** to promote "reduce their environmental impact" of automobile.
###### - **"Whether receiving subsidy or not"** depends on two indicators: **"CO2 emissions"** and **"TMR(Total Material Requirement)"** in the one automobile's life cycle.

---

# So, in the case, causal diagram is below.

![bg 80%](causal_diagram_collider_CO2_TMR.drawio.png)
![bg 80%](CO2_x_TMR_y.png)
<!-- left figure shows that ... -->
<!-- So, "receive subsidy or not" is collider of X and Y -->
<!-- right figure shows that ... -->
<!-- the values of CO2 and TMR is standardized to have mean 0.0 & variance 1.0 -->
<!-- blue plot is..., green plot is ... -->
---

##### So, in order to promote this subsidy program, **we selected data at the only successful companies(left figure)** and tried to find their characteristics.

##### => A **negative correlation** between CO2 emission and TMR is happened!

##### =>Is there a trade-off between CO2 emission and TMR? Does improving one worsen the other?

![bg left:35% 100%](CO2_x_TMR_y_selected.png)

### =>Actually, this is "collider bias" in data collection!

---

## this is one of "collider bias"!

![bg left:40% 100%](CO2_x_TMR_y.png)
![bg left:40% 100%](CO2_x_TMR_y_selected.png)

###### - Originally, **there is no correlation(相関) & causation(因果)** between "CO2 emission" and "TMR". (i.e. basically, they are not "trade off"!)

###### - However, **by selecting(選択) data at the "collider"**, correlation(相関) is happend without causation(因果).

##### In case of **"collider bias" by selecting(選択)**, relatively easy to imagine, right??

---

### Next, let's try to check "collider bias" by adjusting(調整) data at collider through the regression analysis:)

#### - the example of "triathlon" and "duathlon":

---

#### The causal diagram around "triathlon" and "duathlon"

### So, in order to estimate **the causal effect of "bike ability($X_1$)"=>"time of duathlon($t_{dual}$)"**, what factors should we inclode to regression analysis???

![bg right:40% 100%](causal_diagram_triathlon.drawio.png)

---

### Generating dataset & check the answer

###### the setting for generating data is bellow.

###### - 1. "bike_ability($X_1$)", "run_ability($X_2$)", and "swim_ability($X_3$)" is independent(i.e. no correlation each other)

###### - 2. "time of duathlon($t_{dual}$)" is depend on $X_1$, $X_2$, and random term($\varepsilon_{dual}$)

$$
t_{dual} = -0.8\times X_1 - 1.5 \times X_2 + \varepsilon_{dual}
$$

###### - 3. "time of triathlon($t_{triple}$)" is depend on $X_1$, $X_2$, $X_3$, and random term($\varepsilon_{triple}$)

$$
t_{triple} = -1.0\times X_1 - 0.8 \times X_2 - 0.8 \times X_3+ \varepsilon_{triple}
$$

---

# Generated dataset is below.

![bg left:55% 100%](triathlon_pairplots.png)

---
If you wanna try this experiment, you can also generate the dataset.
```python
# set the num of sample data
N = 5000

# Firstly generated data of 'bike_ability', 'run_ability','swim_ability'
# Each abilities are generated by Normal distribution of mu=0.0 & sigma=1.0
bike_ability = np.random.normal(loc=0.0, scale=1.0, size=N)
run_ability = np.random.normal(loc=0.0, scale=1.0, size=N)
swim_ability = np.random.normal(loc=0.0, scale=1.0, size=N)

# Secondly, 'duathlon_times' is generated by 'bike_ability', 'run_ability'
# generate error term for 'duathlon_time'
error_1 = np.random.normal(loc=0, scale=1.0, size=N)
# we set 'duathlon_times' ＝ -0.8×'bike_ability' - 1.5×'run_ability'＋ error term
duathlon_times = -0.8 * bike_ability - 1.5 * run_ability + error_1

# Thirdly、'duathlon_times' is generated by 'bike_ability', 'run_ability', 'swim_ability'
# generate error term for 'triathlon_time'
error_2 = np.random.normal(loc=0, scale=1.0, size=N)
# we set 'duathlon_times' ＝ -1.0×'bike_ability' - 0.8×'run_ability' -0.8＋ error term
triathlon_time = -1 * bike_ability - 0.8 * run_ability - 0.8 * swim_ability + error_2

# Integrate all data we generated as a DataFrame
df_du_tri = pd.DataFrame(
    data={
        'bike_ability':bike_ability,
        'run_ability':run_ability,
        'swim_ability':swim_ability,
        'duathlon_time':duathlon_times,
        'triathlon_time':triathlon_time
    }
)

# check the content of DataFrame
df_du_tri.head()
```

---

###### Our objective is estimating **"the causal effect of $X_1$ =>$t_{dual}$"**. So, firstly, I tried single linear regression:

###### - Explanatory variables = [$X_1$]

###### - Explained variable = $t_{dual}$

$$
t_{dual} \sim Normal(\mu = a_0 +  a_1 \times X_1, \sigma^2)
$$

![bg right:40% 100%](causal_diagram_triathlon.drawio.png)

###### using this formula and datasets(5000 samples), we estimated $a_0$, $a_1$, $\sigma^2$.

###### After estimation, let's check **whether $\hat{a_1}$ is close to $-0.8$(=actula causal effect)** or not.

---

### The result of single linear regression analysis is ...

$$
t_{dual} \sim Normal(\mu = a_0 +  a_1 \times X_1, \sigma^2)
$$

![bg right:40% 100%](causal_diagram_triathlon.drawio.png)

###### $\hat{a_1} = - 0.823$. This value is **close to $-0.8$(=actula causal effect)**

###### So here, the causal effect of "$X_1$ -> $t_{dual}$" **is  properly estimated** by a single regression with "bicycle power($X_1$)" as the only explanatory variable.
###### In this case, **this simple regression is "necessary and sufficient"!**

---

# So then, what happens if we add explanatory variables here?

![bg 100%](triathlon_pairplots.png)
![bg 100%](causal_diagram_triathlon.drawio.png)


---

#### Let's add "variable that might be related to X(cause) and Y(outcome)!"

###### - Explanatory variables = [$X_1$, $t_{triple}$]
###### - Explained variable = $t_{dual}$

$$
t_{dual} \sim Normal(\mu = a_0 +  a_1 \times X_1 + a_2 \times t_{triple}, \sigma^2)
$$

###### Same with previous model, using this formula and datasets(5000 samples), we estimated $a_0$, $a_1$, $a_2$, $\sigma^2$.

###### After estimation, let's check **whether $\hat{a_1}$ is close to $-0.8$(=actula causal effect)** or not.

![bg right:40% 100%](causal_diagram_triathlon.drawio.png)
<!-- ![bg right:40% 100%](triathlon_pairplots.png) -->


---
### The result is...
$$
t_{dual} \sim Normal(\mu = a_0 +  a_1 \times X_1 + a_2 \times t_{triple}, \sigma^2)
$$
###### $\hat{a_1} = - 0.293$.

###### By adding "triathlon time($t_{triple}$)" to the model, "$\hat{a_1} \neq \text{causal effect}$" (i.e. $Correlation \neq Causation$) is happened!

###### In fact, in this causal diagram, adding the collider "triathlon time($t_{triple}$)" makes "run ability($X_2$)" as a "confounding factor".

![bg right:40% 100%](causal_diagram_triathlon.drawio.png)

---

#### Additional contents: "AIC" vs "estimate causal effect"(dear user of statistics, regression analysis, exc.)

###### this table shows the result of each regression analysis.

| explanatory variables                       | AIC          | $\hat{a_1}$| $abs (0.8- \hat{a_1})$|
|---------------------------------------------|--------------|------------------------------|--------------------------------| 
| [bike_ability]                              | 20261 | -0.848                    | 0.048                   | 
| [bike_ability, triathlon_time]              | 19203 | -0.304                    | 0.496                       | 
| [bike_ability, triathlon_time, run_ability] | 14258 | -0.824                    | 0.024                       | 
| [bike_ability, run_ability]                 | 14256 | -0.827                    | 0.027

---

| explanatory variables                       | AIC          | $\hat{a_1}$| $abs(0.8 - \hat{a_1})$| 
|---------------------------------------------|--------------|------------------------------|--------------------------------| 
| [bike_ability]                              | 20261 | -0.848                    | 0.048                   | 
| [bike_ability, triathlon_time]              | 19203 | -0.304                    | 0.496                       | 
| [bike_ability, triathlon_time, run_ability] | 14258 | -0.824                    | 0.024                       | 
| [bike_ability, run_ability]                 | 14256 | -0.827                    | 0.027

###### [bike_ability] model can estimate causal effect more properly, but AIC is higher than [bike_ability, triathlon_time] model! 
###### This example shows that "**AIC of model is low**" and "**$\hat{a_1}$ is representing the causal effect more properly**" is **essentially different**.:satisfied:

---
# Summary of today's short lecture

##### - Correlation $\neq$ Causation(Causal relation)

##### - When estimating causal effects from regression coefficients in regression analysis,

- ##### (the contents of last short lecture) In case of '**confounding factor**', we **should add them** to the explanatory variables for avoid "confounding(交絡)".
- ##### (the contents of today's short lecture) In case of '**collider**', we **should not add them** to the explanatory variables for avoid "collider bias(合流点バイアス)".

---

## finally...

# Causal Inference has a 2 frameworks: Pearl & Rubin

##### I talked about Pearl's framework

---

## So, for discussing a causal relationship between X&Y, we **should not look at only X&Y**! We should consider the **surrounding causal diagram**(i.e. system thinking):satisfied:

![bg left:40% 100%](因果ダイアグラム_2.drawio.png)

---

<!-- _class: title -->

# Thank you for your listening!

### pls enjoy your profound and interesting analytics life.:satisfied:

#### Reference

- Multiple Regression Viewed from Causal Inference Perspective
  統計的因果推論の視点による重回帰分析, Mahabu Iwasaki
- 岩波データサイエンス vol.3 因果推論-実世界のデータから因果を読む.
- https://www.slideshare.net/takehikoihayashi/ss-73059140
