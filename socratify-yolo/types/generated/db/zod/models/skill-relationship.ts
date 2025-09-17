import { z } from 'zod';
import { SkillMetadataSchema } from '../skill-metadata';

export const SkillRelationshipModelSchema = z.object({
  id: z.number().int(),
  sourceSkillUuid: z.string(),
  targetSkillUuid: z.string(),
  relationshipType: z.enum(['REQUIRES', 'CONTRASTS_WITH', 'SUPPORTS']),
  strength: z.enum(['HARD', 'IMPORTANT', 'HELPFUL']).optional(),
  riskLevel: z.enum(['LOW', 'MEDIUM', 'HIGH']).optional(),
  notes: z.string().optional(),
  metadata: SkillMetadataSchema,
  createdAt: z.date(),
  updatedAt: z.date(),
});
