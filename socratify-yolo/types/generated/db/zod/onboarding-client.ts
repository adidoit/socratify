import { z } from 'zod';

/**
 * Onboarding Client Types
 * 
 * Centralized onboarding types and constants shared between mobile app and web client
 * for consistent onboarding experience across all platforms
 */

/**
 * Domain interface for business domains
 */
export const DomainSchema = z.object({
  name: z.string(),
  emoji: z.string(),
});
export type Domain = z.infer<typeof DomainSchema>;

/**
 * Sector interface for industry sectors
 */
export const SectorSchema = z.object({
  name: z.string(),
  emoji: z.string(),
});
export type SectorProps = z.infer<typeof SectorSchema>;

/**
 * Market interface for investment markets
 */
export const MarketSchema = z.object({
  name: z.string(),
  emoji: z.string(),
});
export type MarketProps = z.infer<typeof MarketSchema>;

/**
 * Goal interface for user goals
 */
export const GoalSchema = z.object({
  name: z.string(),
  emoji: z.string(),
});
export type GoalProps = z.infer<typeof GoalSchema>;

/**
 * Static business domains data
 */
export const businessDomains = [
  { name: "Strategy", emoji: "🎯" },
  { name: "Investing", emoji: "🤑" },
  { name: "Finance", emoji: "💰" },
  { name: "Marketing", emoji: "📣" },
  { name: "Operations", emoji: "⚙️" },
  { name: "Leadership", emoji: "👥" },
  { name: "Tech", emoji: "💻" },
  { name: "Product", emoji: "📦" },
] as const;

/**
 * Static industry sectors data
 */
export const sectors = [
  { name: "Finance", emoji: "🏦" },
  { name: "Healthcare", emoji: "🏥" },
  { name: "Tech", emoji: "💻" },
  { name: "Retail", emoji: "🛍️" },
  { name: "Transport", emoji: "🚗" },
  { name: "Energy", emoji: "⚡" },
  { name: "Media", emoji: "📺" },
  { name: "Real Estate", emoji: "🏠" },
  { name: "Food", emoji: "🍽️" },
] as const;

/**
 * Static investment markets data
 */
export const markets = [
  { name: "Stocks", emoji: "📈" },
  { name: "Bonds", emoji: "📄" },
  { name: "Crypto", emoji: "💰" },
  { name: "Commodities", emoji: "🌽" },
  { name: "Derivatives", emoji: "🎲" },
  { name: "Private Markets", emoji: "💼" },
  { name: "Infra & Real Estate", emoji: "🏠" },
] as const;

/**
 * Static user goals data
 */
export const goals = [
  { name: "Get better", emoji: "📈" },
  { name: "Change jobs", emoji: "🔄" },
  { name: "Get promoted", emoji: "🏆" },
  { name: "Land a job or internship", emoji: "🎤" },
  { name: "Level up at school", emoji: "🎓" },
] as const;

/**
 * User interests configuration
 */
export const InterestsConfigSchema = z.object({
  companies: z.boolean(),
  industries: z.boolean(),
  open: z.boolean(),
});
export type InterestsConfig = z.infer<typeof InterestsConfigSchema>;

/**
 * Feature descriptions for onboarding
 */
export const FeatureDescriptionsSchema = z.object({
  learn: z.string(),
  interviewPrep: z.string(),
  rolePlay: z.string(),
  realPlay: z.string(),
});
export type FeatureDescriptions = z.infer<typeof FeatureDescriptionsSchema>;

/**
 * Complete onboarding persistence state
 * Tracks user progress through the entire onboarding flow
 */
export const OnboardingPersistenceSchema = z.object({
  // Basic goal configuration
  userStartingLevel: z.string(),
  userGoal: z.string(),
  dynamicQuestion: z.string(),
  dynamicGuidance: z.array(z.string()).optional(),
  timestamp: z.string(),
  
  // Skills selection
  selectedSkills: z.array(z.string()).optional().describe('Flat storage of skills selected during onboarding'),
  
  // Interests configuration
  interests: InterestsConfigSchema.optional(),
  interestsTimestamp: z.string().optional(),
  
  // Goal details
  userGoalInputText: z.string().optional(),
  audienceFeedback: z.string().optional(),
  goalDetailsTimestamp: z.string().optional(),
  isAudioInput: z.boolean().optional(),
  
  // Goal synthesis (V4)
  goalSynthesis: z.any().optional().describe('GoalSynthesisV4Response from generated types'),
  goalSynthesisTimestamp: z.string().optional(),
  goalSynthesisError: z.boolean().optional(),
  
  // Processed synthesis data
  synthesizedGoal: z.string().optional(),
  userShortGoal: z.string().optional(),
  
  // Industry selection
  selectedIndustries: z.array(z.string()).optional(),
  industriesTimestamp: z.string().optional(),
  
  // Company selection (V4 feature)
  selectedCompanies: z.array(z.string()).optional(),
  companySelectionTimestamp: z.string().optional(),
  companyAnalysis: z.any().optional().describe('CompanyAnalysis from generated types'),
  
  // Custom company handling
  hasCustomCompany: z.boolean().optional(),
  customCompanyName: z.string().optional(),
  
  // Exercise selection and interaction
  onboardingExercise: z.any().optional().describe('ExerciseFromAPI from generated types'),
  selectedExerciseId: z.string().optional(),
  socratifyQuestions: z.array(z.any()).optional().describe('SocratifyQuestion from generated types'),
  userAnswers: z.array(z.any()).optional().describe('UserAnswer from generated types'),
  coverageChecklist: z.any().optional().describe('CoverageChecklist from exercise-client types'),
  debriefData: z.any().optional().describe('Populated in debrief step'),
  
  // Track creation
  trackUuid: z.string().optional().describe('UUID4 for the created track'),
  
  // Track search (V4 feature)
  selectedTracks: z.array(z.string()).optional(),
  trackSelectionTimestamp: z.string().optional(),
  
  // Feature descriptions (set after skills selection)
  featureDescriptions: FeatureDescriptionsSchema.optional(),
}).describe('Complete onboarding state for persistence across sessions');

export type OnboardingPersistence = z.infer<typeof OnboardingPersistenceSchema>;

/**
 * Onboarding step progress tracking
 */
export const OnboardingStepSchema = z.enum([
  'welcome',
  'goal-selection', 
  'goal-details',
  'interests',
  'goal-synthesis',
  'skills-selection',
  'industry-selection',
  'company-selection',
  'exercise-selection',
  'exercise-interaction',
  'debrief',
  'track-creation',
  'complete'
]);
export type OnboardingStep = z.infer<typeof OnboardingStepSchema>;

/**
 * Onboarding progress state
 */
export const OnboardingProgressSchema = z.object({
  currentStep: OnboardingStepSchema,
  completedSteps: z.array(OnboardingStepSchema),
  totalSteps: z.number().int().min(1),
  progressPercent: z.number().min(0).max(100),
  canGoBack: z.boolean(),
  canSkip: z.boolean(),
  isComplete: z.boolean(),
});
export type OnboardingProgress = z.infer<typeof OnboardingProgressSchema>;

/**
 * Onboarding validation result
 */
export const OnboardingValidationSchema = z.object({
  isValid: z.boolean(),
  missingFields: z.array(z.string()),
  errors: z.array(z.string()),
  canProceed: z.boolean(),
  nextStep: OnboardingStepSchema.optional(),
});
export type OnboardingValidation = z.infer<typeof OnboardingValidationSchema>;