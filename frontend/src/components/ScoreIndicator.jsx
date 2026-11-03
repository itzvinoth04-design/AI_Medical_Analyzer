import React from 'react';
import { HelpCircle } from 'lucide-react';

const ScoreIndicator = ({ score = 80, size = "md" }) => {
  // Color scale based on score
  let strokeColor = "#20B2AA"; // Teal
  if (score >= 80) strokeColor = "#247BA0"; // Medical Blue
  if (score < 50) strokeColor = "#E9A23B"; // Amber

  const radius = size === "lg" ? 42 : 28;
  const strokeWidth = size === "lg" ? 8 : 6;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (score / 100) * circumference;

  return (
    <div className="flex items-center gap-3">
      {/* Circular Progress Gauge */}
      <div className="relative flex items-center justify-center shrink-0">
        <svg
          className="transform -rotate-90"
          width={radius * 2 + strokeWidth * 2}
          height={radius * 2 + strokeWidth * 2}
        >
          {/* Background circle */}
          <circle
            cx={radius + strokeWidth}
            cy={radius + strokeWidth}
            r={radius}
            stroke="#E2E8F0"
            strokeWidth={strokeWidth}
            fill="transparent"
          />
          {/* Filled progress circle */}
          <circle
            cx={radius + strokeWidth}
            cy={radius + strokeWidth}
            r={radius}
            stroke={strokeColor}
            strokeWidth={strokeWidth}
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            fill="transparent"
            className="transition-all duration-1000 ease-out"
          />
        </svg>
        <div className="absolute text-center">
          <span className={`font-extrabold text-primary ${size === "lg" ? "text-xl" : "text-sm"}`}>
            {score}
          </span>
          <span className="text-[10px] text-primary/50 font-semibold block -mt-1">/100</span>
        </div>
      </div>

      <div>
        <div className="text-xs font-bold text-primary flex items-center gap-1">
          <span>Condition Compatibility Score: {score}/100</span>
        </div>
        <div className="text-[11px] text-primary/60 leading-tight mt-0.5 max-w-xs">
          Reflects knowledge-base ontology congruence, <em>not</em> clinical disease probability.
        </div>
      </div>
    </div>
  );
};

export default ScoreIndicator;
