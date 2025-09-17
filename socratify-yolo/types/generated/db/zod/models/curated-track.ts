import { z } from 'zod';
import { SkillMetadataSchema } from '../skill-metadata';

export const CuratedTrackModelSchema = z.object({
  id: z.number().int(),
  trackUuid: z.string(),
  trackName: z.string(),
  trackDescription: z.string().optional(),
  trackCoverImage: z.string().optional(),
  publishedAt: z.date().optional(),
  createdBy: z.string(),
  tags: z.string(),
  metadata: SkillMetadataSchema,
  createdAt: z.date(),
  updatedAt: z.date(),
  trackGoal: z.string(),
  status: z.string(),
});
