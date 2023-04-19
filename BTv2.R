# Data setup function shamelessly stolen from my supervisors
set_up_btm<-function(predictors,winner,loser){
  
  names(predictors)[1]<-"ID"
  predictors<-arrange(predictors,ID)
  row.names(predictors)<-predictors$ID
  names(winner)[1]<-"ID"
  names(loser)[1]<-"ID"
  all<-rbind(winner,loser)
  all$winning<-c(rep("yes",length(winner$ID)),rep("no",length(winner$ID)))
  all$ID<-as.factor(all$ID)
  #all$facehair<-as.factor(all$facehair)
  winner2<-subset(all,all$winning=="yes")
  loser2<-subset(all,winning=="no")
  
  #<sad>
  #winner2$ID<-as.factor(winner2$ID)
  #loser2$ID<-as.factor(loser2$ID)
  #winner2$facehair<-as.factor(winner2$facehair)
  #loser2$facehair<-as.factor(loser2$facehair)
  #predictors$ID<-as.factor(predictors$ID)
  # </sad>
  
  beards<-list(winner=winner2,loser=loser2,predictors=predictors)
  return(beards)
}


library(qvcalc)
library(magrittr)
library(knitr)
library(ggplot2)
library(dplyr)
library(BradleyTerry2)

# setwd("../Other data files/")
winner <- read.csv("Melee winners3.csv")
loser <- read.csv("Melee losers3.csv")
predictors <- read.csv("Melee players.csv")

winner$Characters <- as.factor(winner$Characters)
loser$Characters <- as.factor(loser$Characters)

winner$Matchup <- as.factor(winner$Matchup)
loser$Matchup <- as.factor(loser$Matchup)

winner$ID <- as.factor(winner$ID)
loser$ID <- as.factor(loser$ID)

btmdata <- set_up_btm(predictors,winner,loser)

system.time(BTv1 <- BTm(player1=winner,player2=loser,id="ID",formula=~Characters+ (1|ID),data=btmdata))
summary(BTv1)
hist(BTv1$coefficients)
BTabilities(BTv1)
anova(BTv1, test = "Chisq")

system.time(BTv2 <- BTm(player1=winner,player2=loser,id="ID",formula=~Matchup+ (1|ID),data=btmdata))
summary(BTv2)
hist(BTv2$coefficients)
anova(BTv2, test = "Chisq")

# Function written by Heather Turner, see https://stackoverflow.com/questions/69892656/bradleyterry2-package-in-r-using-null-hypothesis-as-reference-player
goodness_of_fit<-function(BTModel) {
  cf <- coef(BTModel)[!is.na(coef(BTModel))]
  V <- vcov(BTModel)
  ind <- grep("(Characters)|(Matchup)", names(cf))
  chisq <- c(t(cf[ind]) %*% chol2inv(chol(V[ind, ind])) %*% cf[ind])
  df <- length(ind)
  c(chisq = chisq, df = df)  
}

goodness_of_fit(BTv1)
goodness_of_fit(BTv2)

#Now create output graphs
library(tidyverse)

results_1 <- data.frame(summary(BTv1)$fixef)
results_1 <- rbind(results_1, c(0,0,0,0))
rownames(results_1)[25] <- "CharactersFox"

figure_1 <-
  results_1 %>%
  mutate(name = str_replace(rownames(.),
                            pattern = "Characters",
                            replacement = "")) %>%
  mutate(name = fct_reorder(name, desc(Estimate))) %>% 
  ggplot(aes(x = name,
             y = Estimate,
             ymax = Estimate + Std..Error*1.96,
             ymin = Estimate - Std..Error*1.96)) +
  geom_pointrange(size=1) +
  geom_hline(yintercept = 0,
             linetype = "dotted") +
  labs(x = "Character", y = "Ability Score Estimate") +
  theme_classic() +
  theme(axis.text.x = element_text(angle = 45,
                                   hjust = 1))

figure_1 #Stock icons were added to this graph manually using paint

results_2 <-
  data.frame(summary(BTv2)$fixef) %>% 
  mutate(name = str_replace(rownames(.),
                            pattern = "Matchup",
                            replacement = "")) %>% 
  separate(col = name,
           into = c("player", "opponent")) 

results_2_inv <-
  results_2 %>% 
  mutate(temp_player = opponent,
         temp_opponent = player,
         Estimate = -Estimate) %>% 
  select(- c(opponent, player)) %>% 
  rename(opponent = temp_opponent,
         player = temp_player)

results_2 %>% 
  bind_rows(results_2_inv) %>% 
  mutate(player = factor(player,
                         levels = rev(c("Sheik", "Jigglypuff", "Marth", "Falco", "CaptainFalcon", "Fox", "Peach"))),
         opponent = factor(opponent,
                           levels = c("Sheik", "Jigglypuff", "Marth", "Falco", "CaptainFalcon", "Fox", "Peach"))) %>% 
  ggplot() +
  geom_tile(aes(x = opponent,
                y = player,
                fill = Estimate)) +
  scale_fill_gradient2(low = "red",
                       mid = "white",
                       high = "#00bfc4") +
  labs(x = "Opponent",
       y = "Player") +
  scale_x_discrete(position = "top",
                   expand = c(0, 0)) +
  scale_y_discrete(expand = c(0, 0)) +
  theme_classic() +
  theme(panel.background = element_rect(fill = "grey",
                                        colour = "grey"))


# BTv0 <- BTm(player1=winner,player2=loser,id="ID",formula=~(1|ID),data=btmdata)
# summary(BTv0)
# hist(BTv0$coefficients)
# BTabilities(BTv0)