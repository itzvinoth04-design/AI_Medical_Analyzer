import React, { createContext, useContext, useState } from 'react';

const AssessmentContext = createContext(null);

export const AssessmentProvider = ({ children }) => {
  const [rawText, setRawText] = useState('');
  const [selectedSymptoms, setSelectedSymptoms] = useState([]);
  const [severity, setSeverity] = useState('Moderate');
  const [durationDays, setDurationDays] = useState(2);
  const [progressStatus, setProgressStatus] = useState('Unchanged');
  const [patientInfo, setPatientInfo] = useState({
    age: 25,
    gender: 'Unspecified',
    chronicConditions: '',
    allergies: '',
  });
  const [followUpQuestions, setFollowUpQuestions] = useState([]);
  const [followUpAnswers, setFollowUpAnswers] = useState({});
  const [assessmentResults, setAssessmentResults] = useState(null);

  const resetAssessment = () => {
    setRawText('');
    setSelectedSymptoms([]);
    setSeverity('Moderate');
    setDurationDays(2);
    setProgressStatus('Unchanged');
    setFollowUpQuestions([]);
    setFollowUpAnswers({});
    setAssessmentResults(null);
  };

  return (
    <AssessmentContext.Provider
      value={{
        rawText,
        setRawText,
        selectedSymptoms,
        setSelectedSymptoms,
        severity,
        setSeverity,
        durationDays,
        setDurationDays,
        progressStatus,
        setProgressStatus,
        patientInfo,
        setPatientInfo,
        followUpQuestions,
        setFollowUpQuestions,
        followUpAnswers,
        setFollowUpAnswers,
        assessmentResults,
        setAssessmentResults,
        resetAssessment,
      }}
    >
      {children}
    </AssessmentContext.Provider>
  );
};

export const useAssessment = () => useContext(AssessmentContext);
