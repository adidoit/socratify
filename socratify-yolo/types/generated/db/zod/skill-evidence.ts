import { z } from 'zod';

/**
 * Evidence for a single skill assessment attempt
 */
export const SkillEvidenceItemSchema = z.object({
  attemptId: z.string().optional(), // Reference to ExerciseHistory or Conversation
  timestamp: z.string().datetime(),
  proficiencyScore: z.number().min(0).max(100),
  proficiencyLevel: z.enum(['BEGINNER', 'APPRENTICE', 'PRACTITIONER', 'EXPERT', 'TOP_10']),
  context: z.string().optional(), // What exercise/conversation this came from
  confidence: z.number().min(0).max(1).optional(), // AI confidence in assessment
  feedbackNotes: z.string().optional(), // Specific feedback on this attempt
});

/**
 * Array of skill evidence items
 */
export const SkillEvidenceSchema = z.array(SkillEvidenceItemSchema);

export type SkillEvidenceItem = z.infer<typeof SkillEvidenceItemSchema>;
export type SkillEvidence = z.infer<typeof SkillEvidenceSchema>;