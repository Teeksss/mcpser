import { render, screen, fireEvent } from "@testing-library/react";
import TenantSwitcher from "../TenantSwitcher";

test("renders TenantSwitcher and changes tenant", () => {
  const tenants = [
    { id: "1", name: "Tenant1" },
    { id: "2", name: "Tenant2" },
  ];
  const setTenant = jest.fn();
  render(<TenantSwitcher tenant="1" setTenant={setTenant} tenants={tenants} />);
  expect(screen.getByText(/Tenant1/)).toBeInTheDocument();
  fireEvent.mouseDown(screen.getByRole("combobox"));
  fireEvent.click(screen.getByText(/Tenant2/));
  expect(setTenant).toHaveBeenCalledWith("2");
});