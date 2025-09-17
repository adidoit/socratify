import { z } from 'zod';
import { SkillEvidenceSchema } from '../skill-evidence';

export const UserTrackSkillModelSchema = z.object({
  id: z.number().int(),
  clerkId: z.string(),
  trackUuid: z.string(),
  skillUuid: z.string(),
  proficiencyScore: z.number(),
  proficiencyLevel: z.enum(['BEGINNER', 'APPRENTICE', 'PRACTITIONER', 'EXPERT', 'TOP_10']),
  numAttempts: z.number().int(),
  evidenceSummary: SkillEvidenceSchema,
  isSelected: z.boolean(),
  createdAt: z.date(),
  updatedAt: z.date(),
});
