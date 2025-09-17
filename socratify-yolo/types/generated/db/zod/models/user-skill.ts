import { z } from 'zod';
import { SkillEvidenceSchema } from '../skill-evidence';

export const UserSkillModelSchema = z.object({
  id: z.number().int(),
  clerkId: z.string(),
  skillUuid: z.string(),
  proficiencyScore: z.number(),
  proficiencyLevel: z.enum(['BEGINNER', 'APPRENTICE', 'PRACTITIONER', 'EXPERT', 'TOP_10']),
  numAttempts: z.number().int(),
  evidenceSummary: SkillEvidenceSchema,
  lastPracticed: z.date().optional(),
  nextReview: z.date().optional(),
  source: z.string(),
  sourceId: z.string().optional(),
  createdAt: z.date(),
  updatedAt: z.date(),
});
