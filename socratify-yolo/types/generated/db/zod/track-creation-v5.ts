import { z } from 'zod';

/**
 * Track Creation V5 API Types
 * 
 * Enhanced track creation with support for ELI5, Hot Take, and Rapid Fire exercises
 * Extends V4 functionality with more diverse exercise selection
 */

// Exercise origin types including new learn categories
export const ExerciseOriginV5Schema = z.enum([
  'mental_model',
  'business_model',
  'eli5',
  'hot_take',
  'rapid_fire',
  'news',
  'role_specific',
  'fit_interview'
]);
export type ExerciseOriginV5 = z.infer<typeof ExerciseOriginV5Schema>;

// Exercise category for grouping
export const ExerciseCategoryV5Schema = z.enum([
  'learn',
  'realPlay',
  'interview',
  'rolePlay'
]);
export type ExerciseCategoryV5 = z.infer<typeof ExerciseCategoryV5Schema>;

// Learn exercise breakdown for distribution
export const LearnBreakdownSchema = z.object({
  mentalModel: z.number().min(0).describe('Number of mental model exercises'),
  businessModel: z.number().min(0).describe('Number of business model exercises'),
  eli5: z.number().min(0).describe('Number of ELI5 exercises (must be 0 or 2)'),
  hotTake: z.number().min(0).max(1).describe('Number of hot take exercises (0 or 1)'),
  rapidFire: z.number().min(0).max(1).describe('Number of rapid fire exercises (0 or 1)')
});
export type LearnBreakdown = z.infer<typeof LearnBreakdownSchema>;

// Exercise distribution configuration
export const ExerciseDistributionV5Schema = z.object({
  numLearn: z.number().min(0).describe('Total number of learn exercises'),
  numRealPlay: z.number().min(0).describe('Number of real play exercises'),
  numInterview: z.number().min(0).describe('Number of interview exercises'),
  numRolePlay: z.number().min(0).describe('Number of role play exercises'),
  learnBreakdown: LearnBreakdownSchema.optional().describe('Breakdown of learn exercise types')
});
export type ExerciseDistributionV5 = z.infer<typeof ExerciseDistributionV5Schema>;

// Selection constraints for each exercise type
export const SelectionConstraintsV5Schema = z.object({
  eli5: z.array(z.number()).length(2).describe('Allowed counts for ELI5 (e.g., [0, 2])'),
  hotTake: z.tuple([z.number(), z.number()]).describe('Min and max for hot take'),
  rapidFire: z.tuple([z.number(), z.number()]).describe('Min and max for rapid fire'),
  mentalModel: z.tuple([z.number(), z.number()]).describe('Min and max for mental model'),
  businessModel: z.tuple([z.number(), z.number()]).describe('Min and max for business model')
});
export type SelectionConstraintsV5 = z.infer<typeof SelectionConstraintsV5Schema>;

// Track creation request for V5
export const TrackCreationV5RequestSchema = z.object({
  trackUuid: z.string().uuid().describe('Unique identifier for the track'),
  clerkUserId: z.string().min(1).describe('User ID from Clerk authentication'),
  userEmail: z.string().email().describe('User email address'),
  userGoal: z.string().min(1).describe('User\'s career goal'),
  userGoalText: z.string().optional().describe('Extended goal description'),
  userInterests: z.string().optional().describe('User interests (deprecated, use initialSkills)'),
  userStartingLevel: z.string().optional().describe('User\'s starting skill level'),
  originPage: z.string().optional().describe('Page where track creation was initiated'),
  
  // V5 specific: Skills integration
  initialSkills: z.array(z.object({
    name: z.string(),
    category: z.enum(['HARD', 'FLUID', 'SOFT']),
    targetProficiency: z.enum(['BEGINNER', 'APPRENTICE', 'PRACTITIONER', 'EXPERT', 'TOP_10']),
    definition: z.string(),
    rationale: z.string()
  })).describe('Initial skills to focus on'),
  
  laterDevelopmentSkills: z.array(z.object({
    name: z.string()
  })).describe('Skills for later development')
});
export type TrackCreationV5Request = z.infer<typeof TrackCreationV5RequestSchema>;

// Track creation response for V5
export const TrackCreationV5ResponseSchema = z.object({
  success: z.boolean(),
  trackUuid: z.string().uuid().optional(),
  trackId: z.number().optional(),
  count: z.number().describe('Number of exercises in the track'),
  message: z.string().optional(),
  skills: z.object({
    initial: z.number().describe('Number of initial skills'),
    later: z.number().describe('Number of later development skills')
  }).optional(),
  distribution: ExerciseDistributionV5Schema.optional().describe('Exercise distribution breakdown'),
  error: z.string().optional(),
  code: z.string().optional(),
  stage: z.string().optional(),
  details: z.any().optional()
});
export type TrackCreationV5Response = z.infer<typeof TrackCreationV5ResponseSchema>;

// Search result from Upstash
export const UpstashResultV5Schema = z.object({
  id: z.string().optional(),
  score: z.number().optional(),
  metadata: z.object({
    exerciseUuid: z.string().optional(),
    imageUrl: z.string().optional(),
    coverPlainTitle: z.string().optional(),
    coverWittyTitle: z.string().optional(),
    level: z.number().optional(),
    tags: z.string().optional(),
    exerciseType: z.string().optional()
  }).passthrough().optional()
});
export type UpstashResultV5 = z.infer<typeof UpstashResultV5Schema>;

// Search results organized by category
export const SearchResultsV5Schema = z.object({
  learn: z.array(z.any()).describe('All learn exercises including new types'),
  realPlay: z.array(z.any()),
  interview: z.array(z.any()),
  rolePlay: z.array(z.any())
});
export type SearchResultsV5 = z.infer<typeof SearchResultsV5Schema>;

// Selection analysis with detailed breakdown
export const SelectionAnalysisV5Schema = z.object({
  totalCount: z.number(),
  byCategory: z.record(ExerciseCategoryV5Schema, z.number()),
  byOrigin: z.record(ExerciseOriginV5Schema, z.number()),
  averageSearchScore: z.number(),
  diversityScore: z.number().optional().describe('Measure of distribution across exercise types')
});
export type SelectionAnalysisV5 = z.infer<typeof SelectionAnalysisV5Schema>;

// Default selection constraints
export const DEFAULT_SELECTION_CONSTRAINTS_V5 = {
  eli5: [0, 2] as [number, number],
  hotTake: [0, 1] as [number, number],
  rapidFire: [0, 1] as [number, number],
  mentalModel: [1, 2] as [number, number],
  businessModel: [1, 2] as [number, number]
};