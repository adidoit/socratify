import { z } from 'zod';
import { MetaDataSchema } from './meta-data';
import { CoverElementsSchema } from './cover-elements';
import { IntroElementsSchema } from './intro-elements';
import { ImplicationQuestionSchema } from './implication-question';
import { MentalModelSchema } from './mental-model';
import { KeyQuestionSchema } from './key-question';

// Canonical Socratify Exercise (final aggregated payload)
export const SocratifyExerciseSchema = z.object({
  exerciseVersion: z.number().int(),
  exerciseUuid: z.string(),
  exerciseType: z.string(),
  storyType: z.string(),
  metaData: MetaDataSchema,
  coverElements: CoverElementsSchema,
  introElements: IntroElementsSchema,
  implicationQuestion: ImplicationQuestionSchema,
  mentalModel: MentalModelSchema,
  context: z.string(),
  keyQuestion: KeyQuestionSchema,
});

export type SocratifyExercise = z.infer<typeof SocratifyExerciseSchema>;

