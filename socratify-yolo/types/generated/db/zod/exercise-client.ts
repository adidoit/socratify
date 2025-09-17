import { z } from 'zod';

/**
 * Exercise Client Types
 * 
 * Client-side exercise types shared between mobile app and web client
 * for exercise state management, communication feedback, and user interactions
 */

/**
 * Communication feedback badge for user performance
 */
export const CommunicationFeedbackBadgeSchema = z.object({
  name: z.string().describe('Name of the badge (e.g., "Clear", "Concise", etc.)'),
  color: z.string().describe('Color of the badge (e.g., "green", "yellow", etc.)'),
});
export type CommunicationFeedbackBadge = z.infer<typeof CommunicationFeedbackBadgeSchema>;

/**
 * Feedback for a single communication dimension
 */
export const CommunicationFeedbackDimensionSchema = z.object({
  feedback: z.string().describe('Written feedback for the dimension'),
  badges: z.array(CommunicationFeedbackBadgeSchema).describe('Array of badges awarded for this dimension'),
});
export type CommunicationFeedbackDimension = z.infer<typeof CommunicationFeedbackDimensionSchema>;

/**
 * Feedback on user's communication skills across three dimensions
 */
export const CommunicationFeedbackSchema = z.object({
  clarity: CommunicationFeedbackDimensionSchema.describe('Feedback and badges for clarity'),
  conciseness: CommunicationFeedbackDimensionSchema.describe('Feedback and badges for conciseness'),
  coherence: CommunicationFeedbackDimensionSchema.describe('Feedback and badges for coherence'),
});
export type CommunicationFeedback = z.infer<typeof CommunicationFeedbackSchema>;

/**
 * Negative communication badge types
 */
export const NegativeCommunicationBadgeSchema = z.object({
  type: z.enum(['hedges', 'buzzwords', 'fillers', 'fluff']),
  count: z.number().int().min(0),
  examples: z.array(z.string()),
});
export type NegativeCommunicationBadge = z.infer<typeof NegativeCommunicationBadgeSchema>;

/**
 * Positive communication badge types
 */
export const PositiveCommunicationBadgeSchema = z.object({
  type: z.enum(['clear', 'confident', 'specific', 'focused']),
});
export type PositiveCommunicationBadge = z.infer<typeof PositiveCommunicationBadgeSchema>;

/**
 * Communication badges collection
 */
export const CommunicationBadgesSchema = z.object({
  negative: z.array(NegativeCommunicationBadgeSchema),
  positive: z.array(PositiveCommunicationBadgeSchema),
});
export type CommunicationBadges = z.infer<typeof CommunicationBadgesSchema>;

/**
 * Enhanced communication feedback (V2)
 */
export const CommunicationFeedbackV2Schema = z.object({
  feedbackText: z.string(),
  pithyTitle: z.string(),
  userAnswerTranscript: z.string().optional(),
  communicationBadges: CommunicationBadgesSchema.optional(),
});
export type CommunicationFeedbackV2 = z.infer<typeof CommunicationFeedbackV2Schema>;

/**
 * Communication feedback response wrapper
 */
export const CommunicationFeedbackV2ResponseSchema = z.object({
  hotTake: z.string(),
  communicationFeedback: CommunicationFeedbackV2Schema,
});
export type CommunicationFeedbackV2Response = z.infer<typeof CommunicationFeedbackV2ResponseSchema>;

/**
 * Other option for exercise choices
 */
export const OtherOptionSchema = z.object({
  id: z.string(),
  text: z.string(),
  type: z.string(),
});
export type OtherOption = z.infer<typeof OtherOptionSchema>;

/**
 * Single Socratify take item
 */
export const SocratifyTakeItemSchema = z.object({
  details: z.string().describe('Detailed explanation'),
  image: z.string().describe('Image name (for getDimensionImage)'),
  summary: z.string().describe('Short summary displayed in collapsed view'),
  title: z.string().describe('Title of the take'),
});
export type SocratifyTakeItem = z.infer<typeof SocratifyTakeItemSchema>;

/**
 * Coverage area in the coverage checklist
 */
export const CoverageAreaSchema = z.object({
  areaName: z.string(),
  coverage: z.enum(['covered', 'partial', 'none']),
  reasoning: z.string(),
});
export type CoverageArea = z.infer<typeof CoverageAreaSchema>;

/**
 * Coverage checklist response
 */
export const CoverageChecklistSchema = z.object({
  keyAreas: z.array(CoverageAreaSchema),
  totalAreas: z.number().int().min(0),
  coveredCount: z.number().int().min(0),
  summaryText: z.string(),
  userAnswerTranscript: z.string().optional(),
});
export type CoverageChecklist = z.infer<typeof CoverageChecklistSchema>;

/**
 * Track metadata for exercises
 */
export const TrackMetadataSchema = z.object({
  trackUuid: z.string(),
  trackName: z.string(),
  userGoal: z.string(),
  shortRationale: z.string(),
  detailedRationale: z.string(),
});
export type TrackMetadata = z.infer<typeof TrackMetadataSchema>;

/**
 * Exercise history state for client applications
 * Combines canonical exercise history fields with client-specific state
 */
export const ExerciseHistoryStateSchema = z.object({
  // Canonical ExerciseHistoryModel fields
  exerciseUuid: z.string(),
  clerkId: z.string(),
  currentStep: z.string(),
  completedSteps: z.array(z.string()),
  socratifyQuestions: z.array(z.any()), // Use SocratifyQuestion from generated
  userAnswers: z.array(z.any()), // Use UserAnswer from generated
  XPEarned: z.number().int().min(0),
  
  // Client-specific fields
  exerciseHistoryId: z.number().int().optional().describe('Maps to canonical id'),
  storyType: z.string(),
  exerciseType: z.string(), 
  conversationId: z.string().optional(),
  socratifyUserId: z.string().optional(),
  userChoice: z.string().optional(),
  otherOptions: z.array(OtherOptionSchema),
  debriefData: z.any().optional(),
  rapidFireData: z.any().optional(),
  finalConversationData: z.any().optional(),
  socratifyTake: SocratifyTakeItemSchema.optional(),
  rapidReaction: z.string().optional(),
  coverageChecklist: CoverageChecklistSchema.optional(),
  lastUpdated: z.string().optional(),
  hotTake: z.string().optional(),
}).catchall(z.any()).describe('Allow additional exercise fields via extends pattern');

export type ExerciseHistoryState = z.infer<typeof ExerciseHistoryStateSchema>;

/**
 * Default exercise history state
 */
export const DEFAULT_EXERCISE_HISTORY_STATE: ExerciseHistoryState = {
  // Canonical fields
  exerciseUuid: "NOT_SET",
  clerkId: "",
  currentStep: "FEED",
  completedSteps: [],
  socratifyQuestions: [],
  userAnswers: [],
  XPEarned: 0,
  
  // Client-specific fields
  storyType: "NOT_SET",
  exerciseType: "NOT_SET", 
  otherOptions: [],
  hotTake: "",
  rapidReaction: "",
  socratifyTake: undefined,
  debriefData: {},
  rapidFireData: {},
  finalConversationData: {},
  coverageChecklist: undefined,
};

/**
 * Pagination metadata for exercise lists
 */
export const ExercisePaginationSchema = z.object({
  currentPage: z.number().int().min(1),
  totalPages: z.number().int().min(1),
  totalCount: z.number().int().min(0),
  limit: z.number().int().min(1),
  hasNextPage: z.boolean(),
  hasPreviousPage: z.boolean(),
});
export type ExercisePagination = z.infer<typeof ExercisePaginationSchema>;

/**
 * Pagination metadata for exercise lists
 */
export const ExercisePaginationMetaSchema = z.object({
  sortBy: z.string(),
  sortOrder: z.string(),
});
export type ExercisePaginationMeta = z.infer<typeof ExercisePaginationMetaSchema>;

/**
 * Paginated exercise history response 
 */
export const PaginatedExerciseHistoryResponseSchema = z.object({
  data: z.array(z.any()), // Will use ExerciseHistoryWithExercise from generated models
  pagination: ExercisePaginationSchema,
  meta: ExercisePaginationMetaSchema,
});
export type PaginatedExerciseHistoryResponse = z.infer<typeof PaginatedExerciseHistoryResponseSchema>;