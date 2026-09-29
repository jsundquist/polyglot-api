import z from 'zod';

/**
 * An optional UUID query param that also treats an empty string (e.g. `?cursor=`)
 * as "not provided" instead of a validation error - clients that omit the value
 * but still send the key shouldn't get a 400.
 */
export function optionalUuidQuery() {
  return z.preprocess(
    (val) => (val === '' ? undefined : val),
    z.uuidv4().optional(),
  );
}

/** An optional positive-integer query param (e.g. `?limit=`) that treats an empty string as "not provided". */
export function optionalPositiveIntQuery() {
  return z.preprocess(
    (val) => (val === '' ? undefined : val),
    z.coerce.number().positive().optional(),
  );
}

/**
 * Rejects an embedded NUL character, which Postgres text columns reject at
 * the driver level (an uncaught 500, not a clean validation error).
 */
export function noNullBytes<T extends z.ZodString>(schema: T) {
  return schema.refine(
    (val) => !val.includes('\0'),
    'must not contain a NUL character',
  );
}
