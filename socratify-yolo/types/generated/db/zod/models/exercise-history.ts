import { z } from 'zod';
import { SocratifyExerciseSchema } from '../socratify-exercise';
import { SocratifyQuestionSchema } from '../socratify-question';
import { UserAnswerSchema } from '../user-answer';

export const ExerciseHistoryModelSchema = z.object({
  id: z.number().int(),
  exerciseUuid: z.string(),
  clerkId: z.string(),
  createdAt: z.date(),
  currentStep: z.string(),
  finalExerciseData: SocratifyExerciseSchema,
  hotTake: z.string().optional(),
  rating: z.string().optional(),
  updatedAt: z.date(),
  completedSteps: z.array(z.string()),
  socratifyQuestions: z.array(SocratifyQuestionSchema),
  userAnswers: z.array(UserAnswerSchema),
  XPEarned: z.number().int(),
  trackUuid: z.string().optional(),
  feedbackForUser: z.string().optional(),
  skills: z.any().optional(),
});
