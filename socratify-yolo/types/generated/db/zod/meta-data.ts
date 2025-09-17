import { z } from 'zod';

export const MetaDataSchema = z.object({
  generalLevel: z.number().int().min(1).max(5),
  generalLevelDescription: z.string(),
  primaryDomainName: z.string(),
  primaryDomainLevel: z.number().int().min(1).max(5),
  primaryDomainLevelDescription: z.string(),
  secondaryDomainName: z.string(),
  secondaryDomainLevel: z.number().int().min(1).max(5),
  secondaryDomainLevelDescription: z.string(),
  fileName: z.string(),
  faviconUrl: z.string().url(),
  happyPath: z.string(),
  backgroundNeeded: z.string(),
});

export type MetaData = z.infer<typeof MetaDataSchema>;

