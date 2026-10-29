export type ButtonProps = React.ButtonHTMLAttributes<HTMLButtonElement>;

export function cx(...classes: (string | undefined | null | false)[]): string {
  return classes.filter(Boolean).join(' ');
}
