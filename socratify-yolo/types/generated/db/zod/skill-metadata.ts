import { z } from 'zod';

/**
 * Flexible metadata for skills
 * Can be extended with additional fields as needed
 */
export const SkillMetadataSchema = z.object({
  // Display configuration
  icon: z.string().optional(), // Icon name or URL
  color: z.string().optional(), // Hex color for UI
  
  // Learning configuration
  decayRate: z.number().min(0).max(1).optional(), // How fast skill decays (0 = never, 1 = immediately)
  masteryThreshold: z.number().min(0).max(100).optional(), // Score needed for mastery
  minAttemptsForProficiency: z.number().int().min(1).optional(), // Min attempts before advancing
  
  // Content configuration
  exampleCompanies: z.array(z.string()).optional(), // Companies that exemplify this skill
  relatedConcepts: z.array(z.string()).optional(), // Related mental models or concepts
  resources: z.array(z.object({
    title: z.string(),
    url: z.string().url(),
    type: z.enum(['article', 'video', 'book', 'course']).optional(),
  })).optional(),
  
  // Assessment configuration
  assessmentTypes: z.array(z.enum(['conversation', 'exercise', 'quiz', 'project'])).optional(),
  difficultyModifier: z.number().min(0.5).max(2.0).optional(), // Multiplier for difficulty
}).passthrough(); // Allow additional fields for future expansion

export type SkillMetadata = z.infer<typeof SkillMetadataSchema>;