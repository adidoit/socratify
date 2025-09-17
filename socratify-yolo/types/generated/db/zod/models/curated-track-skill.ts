import { z } from 'zod';

export const CuratedTrackSkillModelSchema = z.object({
  id: z.number().int(),
  trackId: z.number().int(),
  skillUuid: z.string(),
  importance: z.enum(['CORE', 'PRIMARY', 'SECONDARY']),
  rationale: z.string().optional(),
  coveragePercent: z.number(),
  createdAt: z.date(),
  updatedAt: z.date(),
});
