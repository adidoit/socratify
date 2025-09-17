import { z } from 'zod';
import { KeyQuestionSchema } from './key-question';

// Exercise type enum for all search tools
export const SearchExerciseTypeSchema = z.enum([
  'business_model',
  'mental_model',
  'eli5',
  'hot_take',
  'rapid_fire',
  'fit_interview',
  'role_specific',
  'real_play'
]);

// Search request schema (common for all tools)
export const SearchToolRequestSchema = z.object({
  query: z.union([z.string(), z.array(z.string())]).describe('Search query or queries'),
  limit: z.number().optional().default(6).describe('Maximum results to return'),
  exclude: z.array(z.string()).optional().describe('Exercise UUIDs to exclude from results')
}).passthrough(); // Allow additional fields

// Union type for keyQuestion (can be string or complex object)
// Note: KeyQuestionSchema needs to be flexible as fields are often optional
export const SearchKeyQuestionSchema = z.union([
  z.string(),
  KeyQuestionSchema.partial().passthrough() // Make all fields optional and allow extras
]);

// Search exercise result schema
export const SearchExerciseResultSchema = z.object({
  exerciseUuid: z.string().describe('Unique exercise identifier'),
  title: z.string().describe('Exercise title'),
  keyQuestion: SearchKeyQuestionSchema.describe('Exercise question - string or object'),
  exerciseType: SearchExerciseTypeSchema.describe('Type of exercise'),
  searchScore: z.number().describe('Search relevance score')
}).passthrough(); // Allow additional fields for forward compatibility

// Response schema (array of results)
export const SearchToolResponseSchema = z.array(SearchExerciseResultSchema);

// Export TypeScript types
export type SearchExerciseType = z.infer<typeof SearchExerciseTypeSchema>;
export type SearchToolRequest = z.infer<typeof SearchToolRequestSchema>;
export type SearchKeyQuestion = z.infer<typeof SearchKeyQuestionSchema>;
export type SearchExerciseResult = z.infer<typeof SearchExerciseResultSchema>;
export type SearchToolResponse = z.infer<typeof SearchToolResponseSchema>;