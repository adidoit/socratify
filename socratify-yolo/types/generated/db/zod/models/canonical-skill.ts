import { z } from 'zod';
import { SkillMetadataSchema } from '../skill-metadata';

export const CanonicalSkillModelSchema = z.object({
  id: z.number().int(),
  skillUuid: z.string(),
  name: z.string(),
  category: z.enum(['HARD', 'FLUID', 'SOFT']),
  definition: z.string(),
  version: z.number().int(),
  status: z.string(),
  parentSkillUuid: z.string().optional(),
  level: z.number().int(),
  beginnerCriteria: z.string(),
  apprenticeCriteria: z.string(),
  practitionerCriteria: z.string(),
  expertCriteria: z.string(),
  top10Criteria: z.string(),
  tags: z.string(),
  metadata: SkillMetadataSchema,
  createdAt: z.date(),
  updatedAt: z.date(),
});
