import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split #for data splitting
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
from keras.models import Sequential   # used for initialize ANN model
from keras.layers import Dense
from sklearn.feature_selection import VarianceThreshold
import pickle
import warnings
warnings.filterwarnings('ignore')
train_set = pd.read_csv('assets/Training.csv')
test_set = pd.read_csv('assets/Testing.csv')
train_set = train_set.iloc[:,:-1]
corr_matrix=train_set.corr()
upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(np.bool))
to_drop = [column for column in upper.columns if any(upper[column] > 0.9)]
train_set=train_set.drop(to_drop, axis=1)
test_set=test_set.drop(to_drop, axis=1)
temp_train=train_set.iloc[:,:-1]
sel = VarianceThreshold(threshold=0.03)
sel.fit(temp_train)
to_drop=[x for x in temp_train.columns if x not in temp_train.columns[sel.get_support()]]
train_set=train_set.drop(to_drop, axis=1)
test_set=test_set.drop(to_drop, axis=1)
encoder = LabelEncoder()
train_set["prognosis"] = encoder.fit_transform(train_set["prognosis"])
test_set["prognosis"] = encoder.transform(test_set["prognosis"])
X_train, X_valid, y_train, y_valid = train_test_split(train_set.drop('prognosis', 1), train_set['prognosis'], test_size = .40, random_state=42,shuffle=True)
test_set = pd.concat([test_set,pd.concat([X_valid,y_valid],axis=1)],axis=0)
dt = DecisionTreeClassifier()
dt.fit(X_train, y_train)
pickle.dump(dt,open('assets/DecisionTree.h5','wb'))
print("Decision Tree Train score with ",format(dt.score(X_train, y_train)))
print("Decision Tree Test score with ",format(dt.score(test_set.iloc[:,:-1], test_set['prognosis'])))
rf = RandomForestClassifier(max_depth=6,oob_score=True,random_state=42,criterion='entropy',max_features='auto',n_estimators=300)
rf.fit(X_train, y_train)
pickle.dump(rf,open('assets/RandomForest.h5','wb'))
print("Random Forest Train score with ",format(rf.score(X_train, y_train)))
print("Random Forest Test score with ",format(rf.score(test_set.iloc[:,:-1], test_set['prognosis'])))

svm = SVC()
svm.fit(X_train, y_train)
pickle.dump(svm,open('assets/SVM.h5','wb'))
print("SVM Train score with ",format(svm.score(X_train, y_train)))
print("SVM Test score with ",format(svm.score(test_set.iloc[:,:-1], test_set['prognosis'])))

bayes = GaussianNB()
bayes.fit(X_train, y_train)
pickle.dump(bayes,open('assets/Naive_bayes.h5','wb'))
print("Naive Bayes Train score with ",format(bayes.score(X_train, y_train)))
print("Naive Bayes Test score with ",format(bayes.score(test_set.iloc[:,:-1], test_set['prognosis'])),'%')

y_train_dum = pd.get_dummies(y_train)
classifier = Sequential()

classifier.add(Dense(64, activation = "relu", input_dim = X_train.shape[1]))
# adding second hidden layer
classifier.add(Dense(48, activation = "relu"))
# adding last layer
classifier.add(Dense(y_train_dum.shape[1], activation = "softmax"))

classifier.compile(optimizer = "adam", loss = "categorical_crossentropy", metrics = ["accuracy"])
classifier.summary()

history = classifier.fit(X_train, y_train_dum, epochs = 5, batch_size = 30)
pickle.dump(classifier,open('assets/ANN.h5','wb'))
print("ANN Train score with ",format(history.history['accuracy'][-1]))
prediction = classifier.predict(test_set.iloc[:,:-1])

prediction = [np.argmax(i) for i in prediction ]

print("ANN Test score with ",format(accuracy_score(test_set['prognosis'], prediction)*100),'%')
