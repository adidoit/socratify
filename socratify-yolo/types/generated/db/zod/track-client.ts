import { z } from 'zod';

/**
 * Track Client Types
 * 
 * Centralized track-related types shared between mobile app and web client
 * for track management, generation, and user interfaces
 */

/**
 * Track lifecycle status types
 */
export const TrackStatusSchema = z.enum([
  'pending',
  'active', 
  'archived',
  'deleted'
]);
export type TrackStatus = z.infer<typeof TrackStatusSchema>;

/**
 * Track generation process status types
 */
export const TrackGenerationStatusSchema = z.enum([
  'pending',
  'queued',
  'processing', 
  'completed',
  'failed'
]);
export type TrackGenerationStatus = z.infer<typeof TrackGenerationStatusSchema>;

/**
 * Track visibility types
 */
export const TrackVisibilitySchema = z.enum([
  'private',
  'public', 
  'unlisted'
]);
export type TrackVisibility = z.infer<typeof TrackVisibilitySchema>;

/**
 * Track filters for querying/filtering tracks
 */
export const TrackFiltersSchema = z.object({
  status: z.enum(['active', 'inactive', 'completed']).optional(),
  generationStatus: TrackGenerationStatusSchema.optional(),
});
export type TrackFilters = z.infer<typeof TrackFiltersSchema>;

/**
 * Core Track interface for client applications
 * Flexible structure to handle various API response formats
 */
export const TrackSchema = z.object({
  // Primary identifiers
  id: z.string().optional(),
  uuid: z.string().optional(),
  trackUuid: z.string().describe('The actual UUID field from API'),
  
  // Track metadata
  title: z.string().optional(),
  name: z.string().optional(), 
  trackName: z.string().describe('The actual title field from API'),
  description: z.string().optional(),
  userGoal: z.string().optional(),
  userGoalText: z.string().optional(),
  
  // Visual assets
  imageUrl: z.string().optional(),
  coverImageUrl: z.string().optional(),
  
  // Status tracking
  status: TrackStatusSchema,
  generationStatus: TrackGenerationStatusSchema,
  progressPercent: z.number().min(0).max(100).optional().describe('Progress percentage for track generation'),
  
  // Timestamps
  createdAt: z.string(),
  updatedAt: z.string(),
  
  // User association
  clerkUserId: z.string().optional(),
  
  // Exercise counts
  exerciseCount: z.number().int().min(0).optional(),
  numItems: z.number().int().min(0).optional().describe('Alternative field name for exercise count'),
  completedExerciseCount: z.number().int().min(0).optional(),
  estimatedDuration: z.string().optional(),
}).catchall(z.any()).describe('Allow additional fields for API flexibility');

export type Track = z.infer<typeof TrackSchema>;

/**
 * Pagination metadata for track lists
 */
export const PaginationSchema = z.object({
  total: z.number().int().min(0),
  limit: z.number().int().min(1),
  offset: z.number().int().min(0),
  hasMore: z.boolean(),
});
export type Pagination = z.infer<typeof PaginationSchema>;

/**
 * Paginated tracks response from API
 */
export const PaginatedTracksResponseSchema = z.object({
  success: z.boolean(),
  tracks: z.array(TrackSchema),
  pagination: PaginationSchema,
});
export type PaginatedTracksResponse = z.infer<typeof PaginatedTracksResponseSchema>;

/**
 * Track generation request payload
 */
export const TrackGenerationRequestSchema = z.object({
  clerkUserId: z.string(),
  userGoal: z.string(),
  userInterests: z.string(),
  userGoalText: z.string().optional(),
  numItems: z.number().int().min(1).max(50),
});
export type TrackGenerationRequest = z.infer<typeof TrackGenerationRequestSchema>;

/**
 * Individual exercise within a track
 */
export const TrackExerciseSchema = z.object({
  exerciseUuid: z.string(),
  sequenceNumber: z.number().int().min(1),
  coverPlainTitle: z.string(),
  selectionReason: z.string(),
  shortRationale: z.string(),
  detailedRationale: z.string(),
  skills: z.string().optional().describe('Skills for this exercise'),
  groupIdentifier: z.string().nullable().optional().describe('Group identifier (A, B, C, etc.)'),
});
export type TrackExercise = z.infer<typeof TrackExerciseSchema>;

/**
 * Extended track exercise for workflow processing
 */
export const WorkflowTrackExerciseSchema = TrackExerciseSchema.extend({
  isGenerated: z.boolean().optional(),
  type: z.string().optional(),
  title: z.string().optional(),
  coverElements: z.any().optional(),
  introElements: z.any().optional(),
  implicationQuestion: z.any().optional(),
  mentalModel: z.any().optional(),
  context: z.string().optional(),
  keyQuestion: z.any().optional(),
  tags: z.string().optional(),
  metaData: z.any().optional(),
});
export type WorkflowTrackExercise = z.infer<typeof WorkflowTrackExerciseSchema>;

/**
 * Track generation response with metadata
 */
export const TrackGenerationResponseSchema = z.object({
  success: z.boolean(),
  trackUuid: z.string().optional(),
  trackName: z.string().optional(),
  track: z.array(TrackExerciseSchema).optional(),
  error: z.string().optional(),
  _meta: z.object({
    poolSize: z.number().int().min(0),
    sampleSize: z.number().int().min(0),
    attemptsUsed: z.number().int().min(0),
    timings: z.object({
      databaseSave: z.number().min(0),
      total: z.number().min(0),
    }),
  }).optional(),
});
export type TrackGenerationResponse = z.infer<typeof TrackGenerationResponseSchema>;

/**
 * Track with exercise metadata for display
 */
export const TrackWithMetadataSchema = z.object({
  trackName: z.string(),
  exercises: z.array(TrackExerciseSchema),
});
export type TrackWithMetadata = z.infer<typeof TrackWithMetadataSchema>;

/**
 * Track exercise metadata for display in track context
 */
export const TrackExerciseMetadataSchema = z.object({
  shortRationale: z.string(),
  detailedRationale: z.string(),
  groupIdentifier: z.string().nullable().optional().describe('Group identifier (A, B, C, etc.)'),
  skills: z.string().nullable().optional().describe('Skills for this exercise'),
  trackUuid: z.string(),
  trackName: z.string(),
  trackCoverImage: z.string().nullable(),
  sequenceNumber: z.number().int().min(1),
});
export type TrackExerciseMetadata = z.infer<typeof TrackExerciseMetadataSchema>;

/**
 * API response wrapper for track exercise metadata
 */
export const TrackExerciseMetadataResponseSchema = z.object({
  trackExercise: TrackExerciseMetadataSchema.nullable(),
});
export type TrackExerciseMetadataResponse = z.infer<typeof TrackExerciseMetadataResponseSchema>;