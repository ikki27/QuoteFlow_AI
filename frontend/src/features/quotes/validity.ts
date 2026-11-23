// Quote validity dates are calendar days in Europe/Ljubljana (the database uses the same "today").
export const VALIDITY_DAYS = 30;
export const today = () => new Date().toLocaleDateString('sv-SE', { timeZone: 'Europe/Ljubljana' });
export function defaultValidity(days = VALIDITY_DAYS) {
 const d = new Date(`${today()}T00:00:00Z`);
 d.setUTCDate(d.getUTCDate() + days);
 return d.toISOString().slice(0, 10);
}
/** Why a draft cannot be sent because of its validity date, or '' when the date is fine. */
export const validityProblem = (validTo: string | null) =>
 !validTo ? 'Pred pošiljanjem vnesite datum veljavnosti (Velja do).'
 : validTo < today() ? 'Datum veljavnosti je že pretekel. Vnesite nov datum (Velja do).' : '';
