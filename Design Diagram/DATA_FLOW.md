#Data Flow

flowchart TD

Start --> AskBudget
AskBudget --> AskOS
AskOS --> FilterPhones
FilterPhones --> FeatureVariance
FeatureVariance --> AskFeatureImportance
AskFeatureImportance --> ComputeScores
ComputeScores --> RankPhones

RankPhones --> ShowTop3
